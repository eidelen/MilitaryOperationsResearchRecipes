import math
import scipy.optimize as opt

# necessary on korean pc?!
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

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
    for line in sensors:
        sqDist += dist_pnt2line(line, point) ** 2
    return sqDist


if __name__ == "__main__":
    print("Multi Sensor Localization - armasuisse W+T, Adrian Schneider")
    print("############################################################\n")

    # (line definition - line angle, point on line as Landesvermessung LV95 coordinates)
    sensors = [(math.radians(-30), (2615050.2, 1170313.8)),
               (math.radians(55), (2615030.5, 1170021.7)),
               (math.radians(135), (2615367.0, 1170022.6)),
               (math.radians(200), (2615434.7, 1170302.6))]

    # find optimal point with minimizer
    minFunc = lambda optPnt : sensor_errors_accum(sensors, optPnt)
    optRes = opt.minimize(minFunc, [0, 0], options={'disp': False})
    print("Optimal location: ", optRes.x)

    # plot sensors and optimal location
    length = 500
    for angle, origin in sensors:
        originX, originY = origin
        destPntY = math.sin(angle) * length + originY
        destPntX = math.cos(angle) * length + originX
        plt.plot([originX, destPntX], [originY, destPntY], 'b')
        plt.plot([originX],[originY], 'bo')

    plt.plot(optRes.x[0], optRes.x[1], 'rX')
    plt.axis('equal')
    plt.show()
