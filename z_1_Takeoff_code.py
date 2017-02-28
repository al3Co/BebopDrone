#!/usr/bin/python
"""
  Starting for usage at the computer
  
"""
import time
from core.bebop import *
drone=Bebop()

"""
    Starting to Fly (1m)
"""
drone.takeoff()
"""
    Flying Movements
"""
drone.hover()
print "hovering"
time.sleep(2)
"""
    Land
"""
drone.land()