import math
import time
import sys
import struct
import threading
from core.bebop import *

z = threading.Semaphore(3)
drone=Bebop()
file = time.strftime("%Y%m%d-%H%M%S")

flagTrue=True
flagDatafromDrone=False
flagHomePosition=False
flagGPSangle=False
flagVWdata=False
flagStateDataCompleted=True
flagControl=True
flagkill = False
flag_yaw_motion = False
flag_leftwards = False
flag_rightwards = False

lat = 500
lon = 500
alt = 500
float (lat)
float (lon)
float (alt)
yaw = 0
GPSAngle = 0
AngleTol = 4
FFtol = 0.00002
ra2gr = 0.0174532925
GPSaM = 111319
angSubst = None

"""
    THREADS
"""

class Thread_dataUpdate(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    
    def run(self):
        global lat, lon, alt, yaw, flagTrue, cicle, flag_yaw_motion
        while flagTrue:
            z.acquire()
            try:
                drone.update()
                (roll, pitch, yaw) = drone.angle
                (lat, lon, alt) = drone.positionGPS
                if flag_yaw_motion:
                    GPS_Angle()
                    Yaw()
                    AngleReady()
                    spinSide()
                    speed()
            except (TypeError):
                pass
            z.release()

class Thread_Saving(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    
    def run(self):
        global lat, lon, yaw, flagDatafromDrone, flagTrue, LatHome, LonHome, flagkill, alt
        counter_1 = 0
        while flagTrue:
            z.acquire()
            if lat != 500 and lon != 500:
                flagDatafromDrone = True
                f = open(file,'a')
                f.write(str(lat) +'\t'+ str(lon)+'\t'+ str(alt)+'\n')
                f.close()
                time.sleep(1)
            else:
                print "NO GPS"
                flagDatafromDrone = False
                time.sleep(1)
                counter_1=counter_1 + 1
                LatHome = 500.0
                LonHome = 500.0
                if counter_1 == 5:
                    print "NO GPS: EXIT PROGRAM"
                    flagkill = True
                    flagTrue = False
            z.release()

class Thread_Movements(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    
    def run(self):
        global lat, lon, alt, yaw, flagTrue, flagStateDataCompleted, flagDatafromDrone, cicle, flagTrue
        global LatHome, LonHome, flagHomePosition
        global Long1, Rlon, Lati1, Rlat, flagVWdata
        cntr = 1
        if cicle == 1:
            time.sleep(3)
        if flagStateDataCompleted and flagDatafromDrone:
            if cicle == 1 and flagHomePosition == False:
                GPS_Home()
            VirtualWall_Data()
        if cicle == 1:
            time.sleep(1)
        while flagTrue:
            z.acquire()
            if flagVWdata==True:
                Control()
            else:
                if flagDatafromDrone == False:
                    print "Waiting:", self.name
                    time.sleep(1)
                    cntr = cntr +1
                    if cntr == 10:
                        print "Exit from:", self.name
                        flagTrue = False
            z.release()

"""
    SET PARAMETERS
"""

def sethomeparam():
    global flagDatafromDrone, flagHomePosition, flagGPSangle, flagVWdata
    global flagTrue, flagControl, flagStateDataCompleted
    flagDatafromDrone = False
    flagHomePosition = False
    flagGPSangle = False
    flagVWdata = False
    flag_yaw_motion = False
    flagStateDataCompleted = True
    flagTrue = False
    flagControl=True
    print "Setting Home parameters"

"""
    CALCULATIONS
"""

def GPS_Home():
    global lat, lon, flagHomePosition
    global LatHome, LonHome, flagkill, flagTrue
    LatHome=lat
    LonHome=lon
    flagHomePosition=True
    if drone.battery < 31:
        print "Drone Battery:", drone.battery, "be careful to Fly.............."
    elif drone.battery < 25:
        print "TOO LOW BATTERY:", drone.battery,"HALTING PROGRAM"
        sethomeparam()
        flagTrue = False
        flagkill = True
    print "Home position saved", LatHome, LonHome


def VirtualWall_Data():
    global lat, lon, LatPoint_1, LonPoint_1, flagVWdata, flagTrue
    global Long1, Rlon, Lati1, Rlat, LatAnte, LonAnte
    print "VW Data - Drone Battery:", drone.battery
    LatAnte=lat
    LonAnte=lon
    if flagVWdata==False:
        MPoint=abs(LonPoint_1 - LonAnte)
        Long1=LonAnte - (MPoint/2)
        Rlon=(MPoint/2) + 0.00015
        MPoint=abs(LatPoint_1 - LatAnte)
        Lati1=LatAnte - (MPoint/2)
        Rlat=(MPoint/2) + 0.00015
        flagVWdata=True
    if abs(abs(LatAnte)-abs(LatPoint_1))>0.001 or abs(abs(LonAnte)-abs(LonPoint_1))>0.001:
        print "The GPS point given are far away"
        print "Distance between points:",abs(LatAnte-LatPoint_1), "in Latitude",abs(abs(LonAnte)-abs(LonPoint_1)),"in Longitude"
        flagTrue=False
        print "SYSTEM EXIT"


def VirtualWall():
    print "VirtualWall"
    global roll, pitch, yaw, lat, lon, alt, LatAnte, LonAnte
    global Long1, Rlon, Lati1, Rlat,speedF,limit, LatPoint_1, LonPoint_1
    distanceHome = math.sqrt ((lat-LatAnte)**2 + (lon-LonAnte)**2)
    distancePoint = math.sqrt((lat-LatPoint_1)**2 + (lon-LonPoint_1)**2)
    if (distanceHome + distancePoint) > limit or alt > 2.5:
        print "Points ",distanceHome+distancePoint," > limit ",limit
        print "Out of safe zone. Current data ", lat, lon, " GPS Point ",LatPoint_1,LonPoint_1, " GPS Home ",LatAnte,LonAnte, " Altitude ",alt,"Distance between Current data to GPS Point", abs(lat-LatPoint_1), abs(lon-LonPoint_1), "Distance between Current to GPS Home",abs(lat-LatAnte),abs(lon-LonAnte)
        if Flag_Fwd==True:
            drone.update( cmd=movePCMDCmd( True, 0, -speedF, 0, 0 ) )
            time.sleep(1.5)
        print "Exiting program out of safe zone"
        drone.update( cmd=movePCMDCmd( False, 0, 0, 0, 0 ) )
        time.sleep(1)
        drone.land()
        flagkill = True
        flagTrue = False
        sethomeparam()
        sys.exit(0)

"""
    CONTROL FLYING CODE
"""

def Control():
    global flagControl, flagDatafromDrone, flagHomePosition, flagGPSangle, flagVWdata
    global flagTrue, cicle
    if flagControl:
        flagControl=False
        try:
            print "Starting movements Drone point", cicle
            if cicle == 1:
                drone.takeoff()
                drone.flyToAltitude(1.0, timeout=5)
                time.sleep(1)
            FlyingToPoint()
        except:
            flagTrue=False
        finally:
            flagTrue=False

"""
    FLYING CODE
"""
def GPS_Angle():
    global lon, alt, LatPoint_1, LonPoint_1, flagGPSangle
    global GPSAngle, flagStateDataCompleted, cicle, latpas, lonpas
    if flagGPSangle==False and cicle == 1:
        GPSAngle = math.atan2((LatPoint_1-lat),(LonPoint_1-lon))
        flagGPSangle = True
        flagStateDataCompleted = False
    elif flagGPSangle==False and cicle > 1:
        GPSAngle = math.atan2((LatPoint_1-latpas),(LonPoint_1-lonpas))
        flagGPSangle = True
        flagStateDataCompleted = False
    else:
        print 'error on GPS Angle'

def Yaw():
    #VirtualWall()
    global yaw, GPSAngle, angSubst, yaw_rotado
    #yaw_rotado = -yaw + (math.pi/2)
    if yaw < -(math.pi/2):
        yaw_rotado = (((3/2)*math.pi + yaw)* -1)-(math.pi/2)
    else:
        yaw_rotado = -yaw + (math.pi/2)
    #diferencia ente angulos
    if yaw_rotado >= 0 and GPSAngle >= 0:
        yaw_new = abs(GPSAngle - yaw_rotado)
    elif yaw_rotado < 0 and GPSAngle < 0:
        yaw_new = abs(abs(GPSAngle) - abs(yaw_rotado))*(-1)
    else:
        yaw_new = abs(abs(GPSAngle)+abs(yaw_rotado))
        if yaw_new > math.pi:
            yaw_new = (2*math.pi) - yaw_new
    angSubst=yaw_new
    #print "GPS Angle:", GPSAngle, "Yaw Drone", yaw, "Substract angle:  -->", angSubst

def spinSide():
    global GPSAngle, yaw_rotado, flag_leftwards, flag_rightwards
    #DRONE
    if yaw_rotado < 0:
        yaw_360 = 2 * math.pi + yaw_rotado
    else:
        yaw_360 = yaw_rotado
    #GPS
    if GPSAngle < 0:
        GPS_360 = 2 * math.pi + GPSAngle
    else:
        GPS_360 = GPSAngle
    #Calcule
    if (yaw_360 > GPS_360) and (yaw_360 <= (GPS_360 + math.pi)):
        #print "Clock wise, rightwards"
        flag_leftwards = False
        flag_rightwards = True

    elif (yaw_360 > (GPS_360 + math.pi)) or (yaw_360 < GPS_360):
        #print "Anti clock wise, leftwards"
        flag_rightwards = False
        flag_leftwards = True
    else:
        print "Error on mathematics"
        flag_rightwards = False
        flag_leftwards = True

def AngleReady():
    global angSubst, AngleTol, Flag_AngleReady, yaw, ra2gr, flag_leftwards, flag_rightwards, yaw_rotado
    #print "Angle Ready(Function)", "Angle: ", angSubst, "must be less than: ", (0.0174532925*AngleTol)
    tmp1 = GPSAngle + (AngleTol * ra2gr)
    tmp2 = GPSAngle - (AngleTol * ra2gr)
    if yaw_rotado < tmp1 and yaw_rotado > tmp2:
        Flag_AngleReady = True
        AngleTol = 2
        flag_rightwards = False
        flag_leftwards = False
    else:
        Flag_AngleReady = False


def speed():
    global lat, lon, LatPoint_1, LonPoint_1, GPSAngle, angSubst, speedY, speedF
    #speedY 25-99
    speedY=abs(int(((100/ math.pi) * angSubst)))
    if speedY < 25:
        speedY = 25
    elif speedY > 99:
        speedY = 99
    #speedF 25-99
    speedF=int((math.sqrt((lat - LatPoint_1)**2 + (lon - LonPoint_1)**2))* 70710.67812)
    if speedF < 25:
        speedF = 25
    elif speedF > 99:
        speedF = 99
    #print "Yaw Speed: ",speedY,"Forward Speed: ",speedF

def FlyingToPoint():
    global lat, LatPoint_1, lon, LonPoint_1, speedF, cicle, FFtol, flag_yaw_motion
    global Flag_AngleReady, Flag_Fwd, DistanceTot
    print "Flying to point", cicle, "Started"
    distlat = None
    distlon = None
    Flag_Fwd = False
    Flag_AngleReady = False
    flag_yaw_motion = True
    time.sleep(1)
    YawMotion()
    print "Flying forward, GOING TO POINT:", cicle, LatPoint_1, LonPoint_1,"From",lat,lon
    distlat = abs(abs(LatPoint_1) - abs(lat))
    distlon = abs(abs(LonPoint_1) - abs(lon))
    if distlat < FFtol and distlon < FFtol:
        print "You are too near of the point", cicle, ", tolerance:", FFtol
    elif cicle == 1:
        while distlat > FFtol and distlon > FFtol:
            distlat = abs(abs(LatPoint_1) - abs(lat))
            distlon = abs(abs(LonPoint_1) - abs(lon))
            Flag_Fwd=True
            if Flag_AngleReady:
                drone.update( cmd=movePCMDCmd( True, 0, speedF, 0, 0 ) )
            else:
                YawMotion()
        print "Done"
    elif cicle > 1:
        MoveXYZcalculation()
        dX = DistanceTot
        drone.moveBy( dX, 0, 0, 0)
    if Flag_Fwd:
        drone.update( cmd=movePCMDCmd( True, 0, -speedF, 0, 0 ) )
        time.sleep(2)
        print "POINT:", cicle, "DONE!!!"
        print "POINT:", cicle, "DONE!!!"
        print "Point:", cicle, ", arrived. Diference LAT:",LatPoint_1 - lat ,"diference LON:",LonPoint_1 - lon
    Flag_Fwd = False
    Flag_AngleReady = False
    drone.update( cmd=movePCMDCmd( False, 0, 0, 0, 0 ) )

def MoveXYZcalculation():
    global LatPoint_1, LonPoint_1, latpas, lonpas
    global DistanceTot
    DistanceTot = math.sqrt((LonPoint_1 - lon)**2 + (LatPoint_1 - lat)**2)
    DistanceTot = DistanceTot * GPSaM
    print 'Distance:', DistanceTot


def YawMotion():
    global speedY, speedF, angSubst, Flag_AngleReady, ra2gr, Flag_Fwd, flag_leftwards, flag_rightwards, AngleTol
    # Hacia que lado
    if flag_leftwards == True and Flag_Fwd == False:
        while Flag_AngleReady == False: #Mientras no este cerca del angulo
            drone.update( cmd=movePCMDCmd( False, 0, 0, -speedY, 0 ) )
            #print "Yaw motion Anti-CW, Drone Angle vs Point:",angSubst ,"greater than:", ra2gr*AngleTol
    
    elif flag_rightwards == True and Flag_Fwd == False:
        while Flag_AngleReady == False: #Mientras no este cerca del angulo
            drone.update( cmd=movePCMDCmd( False, 0, 0, speedY, 0 ) )
            #print "Yaw motion CW, Drone Angle vs Point:",angSubst ,"greater than:", ra2gr*AngleTol

    elif flag_leftwards == True and Flag_Fwd == True:
        while Flag_AngleReady == False:
            drone.update( cmd=movePCMDCmd( True, 0, speedF, -speedY, 0 ) )
            print "Ajustando angulo"
            #print "Yaw motion Anti-CWAND FLYING FORWARD, Drone Angle vs Point:",angSubst ,"greater than:", ra2gr*AngleTol

    elif flag_rightwards == True and Flag_Fwd == True:
        while Flag_AngleReady == False:
            drone.update( cmd=movePCMDCmd( True, 0, speedF, speedY, 0 ) )
            print "Ajustando angulo"
            #print "Yaw motion CW and FLYING FORWARD, Drone Angle vs Point:",angSubst ,"greater than:", ra2gr*AngleTol

"""
    MAIN PATH PLANNING
"""

def mainPP(LatPoint, LonPoint, cicl, latpasado, lonpasado):
    global LatPoint_1, LonPoint_1, cicle, flagTrue, flagControl, LatHome, LonHome
    global flagkill, latpas, lonpas
    cicle = cicl
    LatPoint_1 = LatPoint
    LonPoint_1 = LonPoint
    latpas = latpasado
    lonpas = lonpasado
    if cicle is None:
        print "Sending to Land ..."
        drone.land()
        sys.exit(0)
    try:
        a = Thread_dataUpdate("DataAcquiring_Thread")
        b = Thread_Saving("SavingPosition_Thread")
        c = Thread_Movements("Movements_Thread")
        a.start()
        b.start()
        c.start()
        a.join()
        b.join()
        c.join()
    except(Traceback,UnboundLocalError):
        print "Error on threads"
        flagTrue = False
        flagControl = True
    finally:
        print "Finally"
        flagTrue=False
        sethomeparam()
        print "EXIT POINT:", cicle
    return LatHome, LonHome, flagkill


def mainPrueba(lat, lon, cicle, latpasado, lonpasado):
    print lat, lon, cicle, latpasado, lonpasado
    if latpasado is not None:
        DistanceTot = math.sqrt((lonpasado - lon)**2 + (latpasado - lat)**2)
        DistanceTot = DistanceTot * GPSaM
        print 'Distance:', DistanceTot

if __name__ == "__main__":
    mainPrueba()


#Modifications made
# 1) Rotate side, left, right or error, function def spinSide ()
# 2) Angle rotation tolerance modification and lower AnguleReady flag, AngleReady def function ()
# 3) Modification of FFtol = 0.00004 to FFtol = 0.00002
# 4) Modification of speed speedF and speedY function def speed ()
# 5) Move by "MoveBy" between points
