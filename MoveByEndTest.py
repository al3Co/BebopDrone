#!/usr/bin/python
"""
    Starting for usage at the computer
    Do not delete the except Typer error. GPS data error, added when include GPS
"""
import time
import math
import sys
import signal
import inspect

from core.bebop import *
drone=Bebop()

dX = 0
dY = 0
dZ = 0
dPsi = math.pi/4

def testFly2():
    try:
        drone.takeoff()
        drone.wait( 1.0 )
        drone.hover()
        for i in range (0,4):
            drone.wait( 3.0 )
            drone.moveBy( dX, dY, dZ, dPsi)
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

def testFly():
    signal.signal(signal.SIGINT, signal_handler)
    try:
        drone.takeoff()
        time.sleep(1)
        drone.hover()
        for i in range (0,4):
            time.sleep(3)
            drone.moveBy( dX, dY, dZ, dPsi)
        time.sleep(1)
        drone.hover()
        drone.land()
        sys.exit(0)
    except (TypeError):
        pass

def signal_handler(signal, frame):
    drone.update( cmd=navigateHomeCmd( 0 ) )
    print('You pressed Ctrl+C!')
    print('Landing')
    drone.hover()
    if drone.flyingState is None or drone.flyingState == 1: # taking off
        drone.emergency()
    drone.land()
    sys.exit(0)


if __name__ == "__main__":
    testFly()
