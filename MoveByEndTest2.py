#!/usr/bin/python
"""
    Starting for usage at the computer
"""
import time
import math
from core.bebop import *

drone=Bebop()

dX = 0
dY = 0
dZ = 0
dPsi = math.pi/2

readyFlag = True

def moveByFunction():
    try:
        drone.takeoff()
        drone.wait( 1.0 )
        drone.hover()
        for i in range (0,4):
            drone.moveBy( dX, dY, dZ, dPsi)
            moveByControl()
        drone.wait( 1.0 )
        drone.hover()
        drone.land()
        sys.exit(0)
    except ManualControlException, e:
        print
        print "ManualControlException"
        if robot.flyingState is None or robot.flyingState == 1: # taking off
            # unfortunately it is not possible to land during takeoff for ARDrone3 :(
            robot.emergency()
        robot.land()

def moveByControl():
	while readyFlag:
		drone.update()
		try:
			(dX, dY, dZ, dPsi, Event) = drone.moveByEnd
			if Event == 0:
				print "Drone moved [mts]:", dX, dY, dZ, dPsi
				readyFlag = False
		except Exception, e:
			print "Some error:", e
			pass
	readyFlag = True
	drone.wait( 1.0 )

if __name__ == "__main__":
    moveByFunction()
