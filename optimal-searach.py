import math
import numpy as np
import random
import matplotlib.pyplot as plt

def doOptSearch():
    print("Optimal Search Strategy - armasuisse W+T")

    # define parameters
    w = 200  # m
    v = 10   # m/s
    t = 5 * 60 * 60 # s
    areas = [("A1", "urban", 14100000, 0.6), ("A2", "mountain", 6300000, 0.03), ("A3", "mountain", 4100000, 0.03),
             ("A4", "water", 3500000, 0.15), ("A5", "water", 1900000, 0.15), ("A6", "mountain", 9100000, 0.03)]

    nAreas = len(areas)

    print("w=" + str(w) + " m, v=" + str(v) + " m/s, t=" + str(t) + " s")
    for area_name, area_type, area_size, prop in areas:
        print(area_name + ": " + area_type + ", " + str(area_size) + " m^2, " + "p=" + str(prop))



    #x_t = np.arange(0., 21600, 1)
    #y_t = np.array([randomSearchKoopman(w, v, 16000000, x) for x in x_t])

    #plt.plot(x_t, y_t, 'ro')
    #plt.show()



    maxProb = -1.0;
    maxEffortConf = []

    for x in range(10000000):
        rndEfforts = np.random.rand(nAreas)
        rndEfforts = t / np.sum(rndEfforts) * rndEfforts
        thisRun = computeOverallProbabilityOfDetection(areas, w, v, rndEfforts)
        if thisRun > maxProb:
            maxProb = thisRun
            maxEffortConf = rndEfforts
            print(x, ":", maxProb, maxEffortConf)


def computeOverallProbabilityOfDetection(allAreas, sweepWidth, velocity, efforts):
    probSum = 0

    for ar, ti in zip(allAreas, efforts):
        areaName, areaType, areaSize, areaProp = ar
        probSum = probSum + areaProp * randomSearchKoopman(sweepWidth, velocity, areaSize, ti)

    return probSum


def meanTimeOfDetection(sweepWidth: float, velocity: float, area: float):
    return area / (velocity * sweepWidth) # denoted T in formula


def randomSearchKoopman(sweepWidth: float, velocity: float, area: float, time: float):
    '''
    The probability of detecting a target in given time.
    :param sweepWidth:
    :param velocity:
    :param area:
    :param time:
    :return:
    '''
    return 1.0 - math.exp(-time/meanTimeOfDetection(sweepWidth, velocity, area))

if __name__ == "__main__":
    doOptSearch()