#!/usr/bin/env python

import urllib2
import cv2
import numpy as np
import PIL.Image
import PIL.ImageTk
import copy
import math
import time
import sys
import Tkinter as tk

from main import *

file = time.strftime("puntosGPS")
f = open(file, 'w')

LAT = 25.665330     # INITIAL COORDS
LON = -100.244560
MAPA_ALTITUD = 680    # MARGEN
ZOOM = 19


class MapManager(object): 
    
    
    BASE_URL = "http://maps.googleapis.com/maps/api/staticmap"

    def __init__(self, mapa_altitud, zoom, lat, lon):
        try:
            self.mapa_altitud = mapa_altitud
            self.zoom = zoom
            self.static_map = self.peticion_de_mapa(lat, lon)
            self.img = copy.copy(self.static_map)
            self.centro_lat = lat                 
            self.centro_lon = lon
            self.trazo_puntos = []
        except Exception:
            print 'YOU ARE NOT CONNECTED TO THE INTERNET \ n ---------------------------- \ nfollow the following steps: '
            print '1.- Run this software while connected to the internet '
            print '2.- Once opened disconnect from the internet without closing the window '
            print '3.- Sets connection to Bebop Parrot Drone '
            print '4.- Click on the map to create the route '
            print '5.- Click to send to perform the route or to clear to select again '
            print '--------------------------------------------------------------- \n'
            sys.exit()

    def peticion_de_mapa(self, lat, lon):
        lat = "%s" % lat
        lon = "%s" % lon
        params = (self.BASE_URL, lat, lon, self.zoom, self.mapa_altitud, self.mapa_altitud)
        full_url = "%s?center=%s,%s&zoom=%s&size=%sx%s&sensor=false&maptype=hybrid" % params
        response = urllib2.urlopen(full_url)
        png_bytes = np.asarray([ord(char) for char in response.read()], dtype=np.uint8)
        cv_array = cv2.imdecode(png_bytes, cv2.CV_LOAD_IMAGE_UNCHANGED)
        return cv_array

    @property
    def mapa_en_grados(self):

        deg_lat = self.metros_lineales_mapa/111319.9
        scale = math.cos(self.centro_lat*math.pi/180)
        deg_lon = deg_lat/scale
        return (deg_lat, deg_lon)

    @property
    def metros_lineales_mapa(self): # Metros lineales en el mapa
        
        metros_en_mapa = 591657550.500000 / pow(2, self.zoom+3) # (591657550.500000) es la escala del mapa en nivel 1 de zoom 
        return metros_en_mapa

    def _window_x_y_to_grid(self, x, y):
        
        centro_x = centro_y = self.mapa_altitud / 2
        new_x = x - centro_x
        new_y = -1 * (y - centro_y)
        return new_x, new_y

    def _grid_x_y_to_window(self, x, y):
        centro_x = centro_y = self.mapa_altitud / 2
        new_x = centro_x + x
        new_y = centro_y - y
        return new_x, new_y

    def x_y_to_lat_lon(self, x, y):
        grid_x, grid_y = self._window_x_y_to_grid(x, y)
        compensacion_grados_x = (float(grid_x) / self.mapa_altitud) * self.mapa_en_grados[1]
        compensacion_grados_y = (float(grid_y) / self.mapa_altitud) * self.mapa_en_grados[0]
        return self.centro_lat + compensacion_grados_y, self.centro_lon + compensacion_grados_x

    def lat_lon_to_x_y(self, lat, lon):
        compensacion_grados_lat = lat - self.centro_lat
        compensacion_grados_lon = lon - self.centro_lon
        grid_x = (compensacion_grados_lon / self.mapa_en_grados[1]) * self.mapa_altitud
        grid_y = (compensacion_grados_lat / self.mapa_en_grados[0]) * self.mapa_altitud
        window_x, window_y = self._grid_x_y_to_window(grid_x, grid_y)
        return int(window_x), int(window_y)

    def agrega_waypoint(self, event):  # AGREGA LOS PUNTOS a la tupla (lista)
        x = event.x
        y = event.y
        lat, lon = self.x_y_to_lat_lon(x, y)
        self.plot_point(lat, lon)
        f = open(file,'a')
        f.write(str(lat) +'\t'+ str(lon)+'\n')
        f.close()
        #print lat, lon                    #  impresion de los valores de latitud y longitud
        return lat, lon

    def remueve_waypoint(self, event):   # REMUEVE LOS PUNTOS de la tupla uno por uno (lista)
        try: 
            self.trazo_puntos.pop(-1)  #elimina el ultimo punto dado
            self.img = copy.copy(self.static_map)
        except Exception:
            print 'NO EXISTEN MAS PUNTOS PARA BORRAR \n---------------------------- '    
           
    def limpiar_waypoints(self):     # funcion para Limpiar los puntos 
        self.trazo_puntos = []
        self.img = copy.copy(self.static_map)
        f = open(file, 'w')

    def plot_point(self, lat, lon):  # Va agregando los valores a la lista (lat y lon: plotted_points = [])
        self.trazo_puntos.append([lat, lon])

    def get_plotted_points_as_x_y_list(self): # Devuelve el valor de lat y lon y dibuja las coordenadas en la ventana (x,y)
        return [self.lat_lon_to_x_y(point[0], point[1]) for point in self.trazo_puntos]


class MapGui():   
    
    def __init__(self):
        # Colores preedefinidos para los puntos y lineas 
        self.AMARILLO = cv2.cv.Scalar(0, 300, 400) # segundo o siguientes puntos COLOR AMARILlLO
        self.VERDE = cv2.cv.Scalar(10, 500, 50) # primer punto COLOR VERDE
        self.ROJO = cv2.cv.Scalar(0, 0, 255) # lineas COLOR ROJO              10,500,50 verde | 0 0 255 rojo | 255 255 255 blanco
        #Valores iniciales para las variables
        self.puntos_actuales = 0
        self.puntos_pasados = 'unset' # unset- valor no definido 

        #Creacion de ventana por Tkinter y atributos de esta
        self.root = tk.Tk() #Base para la construccion de la ventana de Tkinter
        self.root.title("MAPA MEDIANTE PUNTOS (COORDENADAS) PARA BEBOP DRONE")
        self.root.resizable(width=False, height=False) # Evita que la ventana pueda expandirse | bloquea boton de maximizar
        self.root.geometry("+%d+%d" % (600,0)) # Posicion de la ventana en la pantalla (x,y)
        setattr(self.root, 'quit_flag', False) #Hace que el programa se cierre
        self.root.protocol('WM_DELETE_WINDOW', self.set_quit_flag)

        #Toma los valores iniciales dados en un principio de LAT y LON para la creacion del mapa 
        self.start_map(LAT, LON) 

        #Creacion de un label para el contador de puntos
        self.texto_de_label = tk.StringVar()
        self.texto_de_label.set('No. De Puntos actuales: %d' %self.puntos_actuales)

        #Configuracion de Botones
        self.botones()

        #Ejecuta todo (clase de MapGui y MapManager)
        self.root.mainloop()

    def set_quit_flag(self):
        #Permite quitar cerrar el programa
        self.root.quit_flag = True

    # Inicia el mapa
    def start_map(self, lat, lon):
        self.map_label = tk.Label(self.root)  #Label que contiene el mapa
        self.map_label.pack()
        self.map = MapManager(MAPA_ALTITUD, ZOOM, lat, lon)  #estos valores son obtenidos al principio 
        self.root.after(0, func=self.loop)
        self.map_label.bind("<Button-1>", self.agrega_punto) # agrega puntos mediante el click izquierdo del mouse
        self.map_label.bind("<Button-3>", self.remueve_punto) # borra puntos mediante el click derecho del mouse

    def agrega_punto(self, event):
        #Agrega puntos
        self.map.agrega_waypoint(event)
        self.puntos_actuales = len(self.map.trazo_puntos) #Devuelve el numero de elementos de la lista - len()
        self.texto_de_label.set('No. De Puntos actuales: %d' %self.puntos_actuales) #inserta el nuevo valor en la etiqueta/label

    def remueve_punto(self, event):
        #Remueve puntos 
        self.map.remueve_waypoint(event)
        self.puntos_actuales = len(self.map.trazo_puntos) #Devuelve el numero de elementos de la lista - len()
        self.texto_de_label.set('No. De Puntos actuales: %d' %self.puntos_actuales) #inserta el nuevo valor en la etiqueta/label
        f = open(file,'r')

    
    def limpia_puntos(self):
        self.map.limpiar_waypoints()
        self.puntos_actuales = 0 #Hace que el valor del label sea cero cuando se pulsa el boton limpiar
        self.texto_de_label.set('No. De Puntos actuales: %d' %self.puntos_actuales)

    def envia_puntos(self):
        #print self.map.trazo_puntos
        #print tuple(self.map.trazo_puntos)
        #print list(self.map.trazo_puntos)
        #print 'Puntos enviados:',len(self.map.trazo_puntos)
        try:
            mainP()
            sys.exit()
        except(TypeError, NameError), e:
            print e
            sys.exit()

    def botones(self):
        #Frame en el que estan contenidos algunos botones en linea y columna del grid
        barra_frame = tk.Frame(self.root, height=100)
              
        etiqueta1 = tk.Label(barra_frame, textvariable=self.texto_de_label, padx=10)
        etiqueta1.pack(side=tk.RIGHT, padx=5, pady=5) #Atributos del label 
        etiqueta1.grid(row=0, column=3, rowspan=2) #Definicion de linea y columna en el que se encuentra el label

        barra_frame.pack(fill='x') #Permite mostrar el Frame 
        #Boton de borrar todos los puntos y atributos de este 
        boton_limpiar = tk.Button(barra_frame, text='Delete Waypoints', command=self.limpia_puntos) #Boton para limpiar puntos
        boton_limpiar.pack(side=tk.LEFT, padx=5, pady=5) #Algunos atributos del boton 'limpiar'
        boton_limpiar.grid(row=0, column=0) #Definicion de linea y columna en el que se encuentra el boton

        boton_enviar = tk.Button(barra_frame, text='Start waypoints with Bebop', command=self.envia_puntos)
        boton_enviar.pack(side=tk.LEFT, padx=5, pady=5)
        boton_enviar.grid(row=0, column=5)

    def loop(self):
        #Bucle principal
        if self.root.quit_flag:
            self.root.destroy() 
        else:
            self.update()
            self.root.after(10, func=self.loop)

    def update(self):
        #Actualiza el mapa para ejercutarse continuamente
        points = self.map.get_plotted_points_as_x_y_list() #Obtiene las coordenadas de la ventana de waypoints
        if self.puntos_pasados == 'unset' or points != self.puntos_pasados: #Se ejecuta si los puntos han cambiado o diferente de nullo
            self.puntos_pasados = points
            for i in range(len(points)): #Actualiza los puntos mediante puntos y lineas(los dibuja)
                if i > 0: #dibuja la linea y los siguientes puntos 
                    cv2.line(self.map.img, pt1=points[i-1], pt2=points[i], color=self.ROJO, thickness = 2)
                    cv2.circle(self.map.img, center=points[i], radius=5, color=self.AMARILLO, thickness=-1)
                else: #Dibuja el punto inicial 
                    cv2.circle(self.map.img, center=points[i], radius=5, color=self.VERDE, thickness=-1)
            #Convierte la imagen de openCV a una imagen de Tkinter
            rgb_img = cv2.cvtColor(self.map.img, cv2.COLOR_BGR2RGB)
            pil_image = PIL.Image.fromarray(rgb_img)
            tk_image = PIL.ImageTk.PhotoImage(image=pil_image)
            self.map_label.configure(image=tk_image)

            self.map_label._image_cache = tk_image 
            self.root.update()

if __name__ == '__main__':
    MapGui()
