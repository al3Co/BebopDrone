#!/usr/bin/python
"""
  Starting for usage at the computer
"""
import time
from core.bebop import *
drone=Bebop()

#define speeds for timed movements
speedR = 20
speedP = 20
speedY = 20
speedG = 20

#Starting to Fly (1m)
drone.takeoff()
time.sleep(1)
print "NOW FLAYING"
drone.hover()

#Fly to altitude (from 1 to 2.5 to 1.5 m)
drone.flyToAltitude(2.5, timeout=20) #20% speed (Verify Bebop.py section flyToAltitude to change speed)
time.sleep(2)
drone.hover()
drone.flyToAltitude(1.5, timeout=20) #20% speed (Verify Bebop.py section flyToAltitude to change speed)
time.sleep(2)
drone.hover()

#Startig timed movements

#drone.update( cmd=movePCMDCmd( active=True, roll=0, pitch=0, yaw=0, gaz=0 ) )
#roll=left/right pitch= Forwards/Backwards yaw=rotation gaz=up/down
drone.update( cmd=movePCMDCmd( True, speedR, speedP, speedY, speedG ) )
time.sleep(3)

#if just rotation or/and up-down movements, Flag as False to keep hovering
drone.update( cmd=movePCMDCmd( False, 0, 0, -speedY, 0 ) )
time.sleep(1)
drone.hover()
print "Stop movements"

#Landing
drone.land()
print "Landed"
