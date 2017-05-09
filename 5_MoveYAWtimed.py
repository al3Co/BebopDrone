#!/usr/bin/python
"""
  Starting for usage at the computer
  The drone takes off, spin for a while and land
"""
import time
import sys
import struct
from bebop import *

drone=Bebop()
speedY = 30

timeout_start = time.time()
timeout = 7

def data_complete():
    global yaw
    drone.update() #get drone data
    (lat, lon, alt)=drone.positionGPS
    (roll, pitch, yaw)=drone.angle
    yaw = yaw * 57.2957795 #Convert rad to deg

def despegar():
    drone.takeoff()
    drone.flyToAltitude(1.5, timeout=20) #20% speed (Verify Bebop.py section flyToAltitude to change speed)
    time.sleep(1)
    drone.hover()
    time.sleep(1)

def SeMueve():
    global yaw
    while time.time() < timeout_start + timeout:
        data_complete()
        drone.update( cmd=movePCMDCmd( False, 0, 0, -speedY, 0 ) )
        print yaw
    print "Stopping movements"
    print "Angle ready: " ,yaw
    drone.hover()
    time.sleep(2)
    drone.land()

if __name__ == "__main__":
    despegar()
    SeMueve()