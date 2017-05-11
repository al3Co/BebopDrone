#!/usr/bin/python
"""
    Starting for usage at the computer
"""
import time
import math
import sys
from core.bebop import *

drone=Bebop()

# Distance to move in [m] and dPsi [rad]
dX = 0
dY = 0
dZ = 0
dPsi = math.pi/2

movDone = True  # Flag to know when movements are done

def moveByFunction():
    try:
        drone.takeoff()
        drone.wait( 1.0 )
        drone.hover()
        for i in range (0,4):   # Try to rotate i times
            print "Movement: ", i
            drone.moveBy( dX, dY, dZ, dPsi) # Command to move to a relative position
            moveByControl() # Stops the movements
	    
        drone.hover()
        drone.wait( 1.0 )
        drone.land()
        sys.exit(0)
    except ManualControlException, e:
        print
        print "ManualControlException"
        if robot.flyingState is None or robot.flyingState == 1: # Taking off
            robot.emergency()
        robot.land()

# While Event != OK or != Interrupted, keep moving
def moveByControl():
	while movDone:
		drone.update()
		try:
			(dX, dY, dZ, dPsi, Event) = drone.moveByEnd
			print "Drone moved [mts, rad]:", dX, dY, dZ, dPsi
			Events = ["OK. Relative displacement done", "UNKNOWN", "BUSY", "NOTAVAILABLE", "INTERRUPTED"]
			print "Move by event", Event, Events[Event]
			if Event == 0 or Event == 5:    # Arrived or Interrupted
                movDone = False
        except Exception, e:    # Catch error
            print "Error getting data from drone, error:", e
            pass
    movDone = True
    drone.wait( 4.0 )  # Waits () secs after arrive to its position

if __name__ == "__main__":
    moveByFunction()

