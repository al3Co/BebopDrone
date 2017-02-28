import time
import sys
import struct
import pygame

pygame.init()
pygame.joystick.init()
js=pygame.joystick.Joystick(0)
flagWhile = True
js.init()
takeoff_flag = False
speed = 30
range = 0.5

print js.get_name()
pygame.event.get()

from core.bebop import *

drone=Bebop()


pygame.time.set_timer(pygame.USEREVENT, 50)

#CAMBIAR POR get_axis(4) "adelante" y get_axis(5) "atras"
#CAMBIAR POR event.axis(4) "adelante" y event.axis(5) "atras"

while flagWhile:
    for event in pygame.event.get():
        
        if event.type == pygame.USEREVENT and takeoff_flag == False:
            if js.get_axis(0) > range or js.get_axis(0) < -range:
                drone.update( cmd=movePCMDCmd( True, speed * js.get_axis(0), 0, 0, 0 ) )
            elif js.get_axis(1) > range or js.get_axis(1) < -range:
                drone.update( cmd=movePCMDCmd( True, 0, speed*(-1)* js.get_axis(1), 0, 0 ) )
            elif js.get_axis(2) > range or js.get_axis(2) < -range:
                drone.update( cmd=movePCMDCmd( True, 0, 0, speed * js.get_axis(2), 0 ) )
            elif js.get_axis(3) > range or js.get_axis(3) < -range:
                drone.update( cmd=movePCMDCmd( True, 0, 0, 0, speed * js.get_axis(3)  ) )
            
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 5:
                print event.button, "Kill program"
                drone.land()
                flagWhile=False
            elif event.button == 12:
                print event.button, "B PRESSED EMERGENCY"
                drone.emergency()
            elif event.button == 13:
                takeoffflag = False
                print event.button, "X PRESSED Land"
                drone.land()
            elif event.button == 14:
                print event.button, "Y Photo taken"
                #drone.takePicture()
            elif event.button == 11:
                takeoffflag = True
                print event.button, "A PRESSED Take off"
                drone.takeoff()
            elif event.button == 0:
                if speed >= 50:
                    speed = speed
                else:
                    speed = speed + 5
                print event.button, "SPEED + 5:", speed
            elif event.button == 1:
                if speed <= 5:
                    speed=speed
                else:
                    speed = speed - 5
                print event.button, "SPEED - 5:", speed

        elif event.type == pygame.JOYAXISMOTION and takeoff_flag == False:
            if event.axis == 0: #Y=1--X=0
                if event.value > range or event.value < -range:
                    drone.update( cmd=movePCMDCmd( True, speed * event.value, 0, 0, 0 ) )
            elif event.axis == 1:
                if event.value > range or event.value < -range:
                    drone.update( cmd=movePCMDCmd( True, 0, speed*(-1)* event.value, 0, 0 ) )
            elif event.axis == 2:
                if event.value > range or event.value < -range:
                    drone.update( cmd=movePCMDCmd( True, 0, 0, speed * event.value, 0 ) )
            elif event.axis == 3:
                if event.value > range or event.value < -range:
                    drone.update( cmd=movePCMDCmd( True, 0, 0, 0, speed * event.value  ) )


