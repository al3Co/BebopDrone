"""
    Create a file with the GPS and Gyroscope data forever each 0.5 secs
"""
import time
from core.bebop import *
drone=Bebop()
file = time.strftime("%Y%m%d-%H%M%S")

while True:
    drone.update()
    (lat, lon, alt)=drone.positionGPS
    (roll, pitch, yaw)=drone.angle
    if lat==500 or lon==500:
        print "No GPS signal"
        time.sleep(1)
    else:
        f = open(file,'a')
        print "GPS data: ", lat, lon, alt, "Gyroscope data:", roll, pitch, yaw, " Saved"
        f.write(str(lat) +'\t'+ str(lon)+'\t'+ str(alt)+'\t'+ str(roll)+'\t'+ str(pitch)+'\t'+ str(yaw)+'\n')
        f.close()
        time.sleep(0.5)
