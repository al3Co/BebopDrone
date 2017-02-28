#!/usr/bin/python
"""
  Starting for usage at the computer
  
"""
import time
from core.bebop import *
drone=Bebop()

speedP = 20
speedR = 20
speedY = 20
speedG = 20

"""
    Starting to Fly (1m)
"""
drone.takeoff()
time.sleep(1)
print "NOW FLAYING"


"""
    Fly to altitude (1 to 2.5 to 1.5 m)
"""
drone.flyToAltitude(2.5, timeout=20) #20% speed (Verify Bebop.py section flyToAltitude to change speed)
time.sleep(2)
drone.trim()

drone.flyToAltitude(1.5, timeout=20) #20% speed (Verify Bebop.py section flyToAltitude to change speed)
time.sleep(2)
drone.trim()

#drone.update( cmd=movePCMDCmd( active=True, roll=0, pitch=0, yaw=0, gaz=0 ) )
#roll=Izquierda/Derecha pitch= Enfrete/Atras yaw=rotacion gaz=Altitud

"""
    Flying Movements
"""
print "Starting movements"
drone.update( cmd=movePCMDCmd( True, speedP, speedR, speedY, speedG ) )
#De norte a Este CW
time.sleep(3)
drone.update( cmd=movePCMDCmd( False, 0, 0, -speedY, 0 ) )
#De norte a Oeste Anti-CW
time.sleep(1)
print "Stop movements"
drone.hover()

"""
    Land
"""
drone.land()
print "Landed"