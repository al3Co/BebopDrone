#!/usr/bin/python
"""
    Starting for usage at the computer
"""
import time
import math
import sys
from core.bebop import *

drone=Bebop()

dX = 0
dY = 0
dZ = 0
dPsi = math.pi/2

movDone = True

def moveByFunction():
    try:
        drone.takeoff()
        drone.wait( 1.0 )
        drone.hover()
        if drone.flyingState == 3: # Flying
        	for i in range (0,4):
            		drone.moveBy( dX, dY, dZ, dPsi)
            		moveByControl()
        drone.hover()
        drone.wait( 1.0 )
        drone.land()
        sys.exit(0)
    except ManualControlException, e:
        print
        print "ManualControlException"
        if robot.flyingState is None or robot.flyingState == 1: # taking off
            robot.emergency()
        robot.land()

def moveByControl():
	while movDone:
		drone.update()
		try:
			(dX, dY, dZ, dPsi, Event) = drone.moveByEnd
			if Event == 0:
				print "Drone moved [mts, rad]:", dX, dY, dZ, dPsi
				movDone = False
		except Exception, e:
			#print "Some error:", e
			pass
	movDone = True
	drone.wait( 1.0 )

if __name__ == "__main__":
    moveByFunction()
