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

dX = 0.5 # 1 mts Forward
dY = 0
dZ = 0
dPsi = 0

def main():
    signal.signal(signal.SIGINT, signal_handler)
    try:
        drone.takeoff()
        time.sleep(1)
        for i in range (0,2):
            drone.moveBy( dX, dY, dZ, dPsi)
            drone.hover()
            time.sleep(1)
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
    main()
