import math


def comp_a(sensors):
    a = 0
    for ang, _, sensorerr in sensors:
        a += math.sin(ang)**2 / sensorerr**2
    return a

def comp_b(sensors):
    b = 0
    for ang, _, sensorerr in sensors:
        b += math.cos(ang)**2 / sensorerr**2
    return b

def comp_h(sensors):
    h = 0
    for ang, _, sensorerr in sensors:
        h += math.sin(ang)*math.cos(ang) / sensorerr**2
    return -h

def comp_f(sensors):
    f = 0
    for ang, linedist, sensorerr in sensors:
        f += linedist*math.sin(ang) / sensorerr**2
    return -f

def comp_g(sensors):
    g = 0
    for ang, linedist, sensorerr in sensors:
        g += linedist*math.cos(ang) / sensorerr**2
    return g

def dist_pnt2line( line, point ):
    lineAngle, pntOnLine = line
    pntLineX, pntLineY = pntOnLine
    pntX, pntY = point
    return math.cos(lineAngle)*(pntLineY-pntY) - math.sin(lineAngle)*(pntLineX - pntX)


def accum_distSQ(lines, point):
    sqDist = 0
    x, y = point
    for lineAng, linePnt, lineAccuracy in lines:
        sqDist += dist_pnt2line((lineAng, linePnt), point) ** 2
    return sqDist


if __name__ == "__main__":
    print("Multi Sensor Localization - armasuisse W+T, Adrian Schneider")
    print("############################################################\n")

    # (line angle, point on line, sensor accuracy (as lower as better))
    sensors = [(0.0, (0.0, 0.0), 1.0),    # y = 0x + 0
               (math.pi / 4, (0.0, 0.0), 1.0)] # y = 1x + 0

    print( accum_distSQ(sensors, (0, 0)) )



