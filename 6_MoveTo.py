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

#CHANGE THIS TO YOUR GPS POINT TO GO
lat = 25.665330
lon = -100.244560
altitude = 2

#press Ctrl+C twice to land
cancelButton = False

def main():
    signal.signal(signal.SIGINT, signal_handler)
    try:
        drone.takeoff()
        time.sleep(2)
        drone.moveTo( lat, lon, altitude)
        time.sleep(10) #??
        drone.hover()
        drone.land()
        sys.exit(0)
    except (TypeError):
        pass

def signal_handler(signal, frame):
    drone.moveToCancel()
    drone.hover()
    print('You pressed Ctrl+C!')
    print('Landing')
    drone.hover()
    if drone.flyingState is None or drone.flyingState == 1: # taking off
        drone.emergency()
    if cancelButton == True:
        drone.land()
        sys.exit(0)
    cancelButton = True




if __name__ == "__main__":
    main()
