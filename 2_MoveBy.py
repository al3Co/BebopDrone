#!/usr/bin/python
"""
    Starting for usage at the computer
    Do not delete the except Typer error. GPS data error, added when include GPS
"""

import time
import sys
import signal
import inspect

from core.bebop import *
drone=Bebop()

dX = 3 # 3 mts Forward
dY = 1 # 1 mts Right
dZ = 0 # 0 mts Down
dPsi = 0 # 0 rad

def main():
    signal.signal(signal.SIGINT, signal_handler)
    try:
        drone.takeoff()
        time.sleep(2)
        drone.moveBy( dX, dY, dZ, dPsi)
        time.sleep(3)
        drone.hover()
        drone.land()
        sys.exit(0)
    except (TypeError) as e:
        pass

def signal_handler(signal, frame):
    drone.update( cmd=navigateHomeCmd( 0 ) )
    print('You pressed Ctrl+C!')
    print('Landing')
    drone.hover()
    time.sleep(1)
    if drone.flyingState is None or drone.flyingState == 1: # taking off
        drone.emergency()
    drone.land()
    sys.exit(0)


if __name__ == "__main__":
    main()


"""
    moveBy
    
    Draft: this command is not implemented yet by the firmware Move the drone to a relative position and rotate heading by a given angle The frame is horizontal and relative to the current drone orientation: - X is front - Y is right - Z is down The movement settings of the device are those set for the autonomous flight.
    
    dX Wanted displacement along the front axis [m]
    dY Wanted displacement along the right axis [m]
    dZ Wanted displacement along the down axis [m]
    dPsi Wanted rotation of heading [rad]
    
    """
