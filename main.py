import time
import sys

from pathplanning import *


cicle=1
LatHome = None
LonHome = None
latpasado = None
lonpasado = None

f = open('puntosGPS')


def mainP():
    global LatHome, LonHome, cicle, kill, latpasado, lonpasado
    for line in f:
        tmp = line.split()
        lat = float(tmp[0])
        lon = float(tmp[1])
        [LatHome, LonHome, kill] = mainPP(lat, lon, cicle, latpasado, lonpasado)
        mainPrueba(lat, lon, cicle, latpasado, lonpasado)
        lonpasado = lon
        latpasado = lat
        cicle = cicle + 1
        if kill:
            sys.exit(0)
        time.sleep(1)
    print 'Home place', LatHome, LonHome
    time.sleep(1)
    cicle = None
    [LatHome, LonHome, kill] = mainPP(lat, lon, cicle, latpasado, lonpasado)


if __name__ == "__main__":
    mainP()