<p align="center">
  <a href="#features">Features</a> |
  <a href="#requirements">Requirements</a> |
  <a href="#documentation">Documentation</a> |
  <a href="#usage">Usage</a> |
  <a href="#communication">Communication</a> |
  <a href="#license">LICENSE</a>
</p>

# Bebop drone
<br />
This code performs the generation of points in the space to realize an autonomous route of precision with a VANT Parrot Bebop 1 or 2.


## Features

- Path planning with map waypoints
- MoveBy
- movePCMD
- XBOX control
- IMU data


## Requirements

### Software

- Python 2.7+
- Numpy
- Tkinter
- OpenCV

### Hardware

- Bebop Drone 1-2 Firmware version: 4.05
- Computer with WiFi connection

## Documentation

Docs:
http://developer.parrot.com/docs/bebop/#general-information

## Usage

### Takeoff

```python
from core.bebop import *
drone=Bebop()

"""
Takeoff (1m)
"""
drone.takeoff()
drone.hover()
time.sleep(2)
"""
Land
"""
drone.land()
```


### PathPlanning

- Connect to the Internet
- Run map.py.
- Placing flight points
- If there is a mistake, click on Delete Waypoints
- To travel, connect to the bebop network, click on Start waypoints with Bebop

### To control the Bebop under code development

In the following order:
- z_1_Takeoff_code.py
- z_MoveBy.py
- z_MoveBy2.py
- z_MoveSpeed.py
- z_getData.py
- z_MoveYAWtimed.py

http://developer.parrot.com/docs/bebop/#general-information

## Communication
- If you found a bug, please open an issue. :bow:
- Also, if you have a feature request, please open an issue. :thumbsup:
- If you want to contribute, submit a pull request.:muscle:

## License
Core data and Copyright:
https://github.com/robotika/katarina
