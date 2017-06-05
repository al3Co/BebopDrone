#!/usr/bin/python
"""
    Starting for usage at the computer
    Do not delete the except Typer error. GPS data error, added when include GPS
"""
import time
import math

start_time = time.time()

from core.bebop import *
drone=Bebop()

def main():
    try:
        drone.takeoff()
        drone.hover()
        time.sleep(5)
        drone.land()
        sys.exit(0)
    except KeyboardInterrupt, e:
        print
        print "ManualControlException"
        drone.hover()
        if drone.flyingState is None or drone.flyingState == 1: # taking off
            drone.emergency()
        drone.land()
        sys.exit(0)

def fixedTime():
    new_time = (((int(math.floor(start_time)) + 1) / 10) + 1) * 10
    print("Wait %s seconds ..." % (new_time - start_time))
    time.sleep(new_time - start_time)
    main()

if __name__ == "__main__":
    fixedTime()
