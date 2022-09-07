import math
import scipy.optimize as opt

def dist_pnt2line(line, point):
    '''
    Shortest distance between a point a line.
    :param line: a line (angle, point on line)
    :param point: a point (x,y)
    :return: minimal distance
    '''
    lineAngle, pntOnLine = line
    pntLineX, pntLineY = pntOnLine
    pntX, pntY = point
    return math.cos(lineAngle)*(pntLineY-pntY) - math.sin(lineAngle)*(pntLineX - pntX)

def sensor_errors_accum(sensors, point):
    '''
    Accumulates the localization error over all sensors.
    :param sensors: all sensors, each having a line and a localization accuracy
    :param point: target location
    :return: accumulated target location error
    '''
    sqDist = 0
    for line, sensorAccuracy in sensors:
        sqDist += dist_pnt2line(line, point) ** 2
    return sqDist


if __name__ == "__main__":
    print("Multi Sensor Localization - armasuisse W+T, Adrian Schneider")
    print("############################################################\n")

    # ((line definition - line angle, point on line), sensor accuracy)
    sensors = [((0.0, (0.0, 5.0)), 1.0),
               ((math.pi / 4, (0.0, 0.0)), 1.0)]

    # find optimal point with minimizer
    minFunc = lambda optPnt : sensor_errors_accum(sensors, optPnt)
    optRes = opt.minimize(minFunc, [10, 10], options={'disp': False})
    print("Optimal location: ", optRes.x)

