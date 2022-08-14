import math
import numpy as np
import itertools
import random
import matplotlib.pyplot as plt
import scipy.optimize as opt

def doOptSearch():
    print("Optimal Search Strategy - armasuisse W+T")

    # define parameters
    w = 200  # m
    v = 10   # m/s
    t = 5 * 60 * 60 # s
    areas = [("A1", "urban", 14100000, 0.40), ("A2", "mountain", 6300000, 0.10), ("A3", "mountain", 4100000, 0.10),
             ("A4", "water", 3500000, 0.15), ("A5", "water", 1900000, 0.15), ("A6", "mountain", 9100000, 0.10)]

    print("w=" + str(w) + " m, v=" + str(v) + " m/s, t=" + str(t) + " s")
    for area_name, area_type, area_size, prop in areas:
        print(area_name + ": " + area_type + ", " + str(area_size) + " m^2, " + "p=" + str(prop))

    solveByTrying(areas, w, v, t)


    #my_constraints = ({'type': 'eq', "fun": apply_sum_constraint})

    #fun = lambda ti: minimizeFunctionProbDetection(areas, w, v, ti)
    #res_cons = opt.minimize(fun, (t/6, t/6, t/6, t/6, t/6, t/6),
    #                             method='SLSQP', options={'disp': True, 'eps': 1}, constraints=my_constraints)

    # print(res_cons)


    # use scipy optimizer

    #bnds = ((0, t), (0, t), (0, t), (0, t), (0, t), (0, t))
    #res = opt.minimize(fun, (t/6, t/6, t/6, t/6, t/6,t/6), method='TNC', bounds=bnds, tol=1e-10, options={'disp': True})

    #print(res)


    #x_t = np.arange(0., 21600, 1)
    #y_t = np.array([randomSearchKoopman(w, v, 16000000, x) for x in x_t])

    #plt.plot(x_t, y_t, 'ro')
    #plt.show()



    # minProb = 1.0;
    # minEffort = []
    #
    # for x in range(1000000):
    #     rndEfforts = np.random.rand(nAreas)
    #     rndEfforts = t / np.sum(rndEfforts) * rndEfforts
    #     thisRun = minimizeFunctionProbDetection(areas, w, v, rndEfforts)
    #     if thisRun < minProb:
    #         minProb = thisRun
    #         minEffort = rndEfforts
    #         print(x, ":", minProb, minEffort)

def solveByTrying(allAreas, sweepWidth, velocity, totalTime):
    nAreas = len(allAreas)

    # generate trials
    x = np.linspace(-1.0, 1.0, num=10)
    trls = [trls for trls in itertools.product(x, repeat=nAreas)]
    nTrials = len(trls)
    iTri = 0
    maxProb = 0
    maxEfforts = []
    amplifiers = np.full(nAreas, totalTime/2.0) # all areas are tried with full effort scale
    bases = np.full(nAreas, totalTime/2.0)
    for solveIters in range(5):

        amplifiers = amplifiers / (solveIters+1)

        print("amp:", amplifiers)
        print("base:", bases)

        for tr in trls:
            # adjust to total invested effort
            iTri = iTri + 1
            nextEfforts = (np.array(tr) * amplifiers) + bases
            nextEfforts = np.clip(nextEfforts, 0.0, totalTime)
            sumNextEfforts = np.sum(nextEfforts)
            if sumNextEfforts > 0.0001:
                nextEfforts = nextEfforts * totalTime / np.sum(nextEfforts)
                detectProb = computeOverallProbabilityOfDetection(allAreas, sweepWidth, velocity, nextEfforts)
                if detectProb > maxProb:
                    maxProb = detectProb
                    maxEfforts = nextEfforts
                    print( iTri, "(", iTri/nTrials*100, ")", ": New best trial: ", maxProb, maxEfforts)

        # adjust base to best solution
        bases = maxEfforts

    print("Best Result: ", maxProb, maxEfforts)







def apply_sum_constraint(inputs):
    # return value must come back as 0 to be accepted
    # if return value is anything other than 0 it's rejected
    # as not a valid answer.
    total = 5 * 60 * 60 - np.sum(inputs)
    return total

def minimizeFunctionProbDetection(allAreas, sweepWidth, velocity, efforts):
    # transform maximize to minimize problem
    optSum = 0

    for ar, ti in zip(allAreas, efforts):
        areaName, areaType, areaSize, areaProp = ar
        optSum = optSum + areaProp * (1.0 - randomSearchKoopman(sweepWidth, velocity, areaSize, ti))

    return optSum


def computeOverallProbabilityOfDetection(allAreas, sweepWidth, velocity, efforts):
    probSum = 0

    for ar, ti in zip(allAreas, efforts):
        areaName, areaType, areaSize, areaProp = ar
        probSum = probSum + areaProp * randomSearchKoopman(sweepWidth, velocity, areaSize, ti)

    return probSum


def meanTimeOfDetection(sweepWidth: float, velocity: float, area: float):
    return area / (velocity * sweepWidth) # denoted T in formula


def randomSearchKoopman(sweepWidth: float, velocity: float, area: float, time: float):
    # The probability of detecting a target in given time.
    return 1.0 - math.exp(-time/meanTimeOfDetection(sweepWidth, velocity, area))

if __name__ == "__main__":
    doOptSearch()