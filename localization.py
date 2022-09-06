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

if __name__ == "__main__":
    print("Multi Sensor Localization - armasuisse W+T, Adrian Schneider")
    print("############################################################\n")

    # (angle, distance to line, sensor accuracy (as lower as better))
    sensors = [(0.0, 1.0, 1.0),
               (math.pi / 2.0, -2.0, 1.0)] # the lines intersect at (2.0, 1.0)

    print(comp_a(sensors), " * x + ", comp_h(sensors), " * y = ", comp_f(sensors))
    print(comp_h(sensors), " * x + ", comp_b(sensors), " * y = ", comp_g(sensors))

    x, y = 0.0, 0.0
    dist = x * math.sin(math.pi / 2.0) - y * math.cos(math.pi / 2.0) + 2.0
    print(dist)


