#!/usr/bin/python
"""
  Takeoff for 4 secs
"""
import time
from core.bebop import *
drone=Bebop()

#Starting to Fly (1m)
drone.takeoff()
time.sleep(4)
drone.hover()
drone.land()
