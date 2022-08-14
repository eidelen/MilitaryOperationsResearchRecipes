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
    t = 10 * 60 * 60 # s
    areas = [("A1", "urban", 14100000, 0.55), ("A2", "mountain", 6300000, 0.05), ("A3", "mountain", 4100000, 0.05),
             ("A4", "water", 3500000, 0.15), ("A5", "water", 1900000, 0.15), ("A6", "mountain", 9100000, 0.05)]

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

    # generate trials
    nAreas = len(allAreas)
    x = np.linspace(-1.0, 1.0, num=10)
    trls = [trls for trls in itertools.product(x, repeat=nAreas)]

    # to narrow in on solution - is adapted during solve iterations
    amplifiers = np.full(nAreas, totalTime / 2.0)
    bases = np.full(nAreas, totalTime / 2.0)

    nSolveIterations = 5
    progress = (len(trls) * nSolveIterations, 0, 1, 0)

    # keep track of best solution
    maxProbability = 0
    bestEfforts = []

    for solveIters in range(nSolveIterations):

        amplifiers = amplifiers / (solveIters+1)

        print("-------------------------------")
        print("amp:", amplifiers)
        print("base:", bases)

        for tr in trls:
            # adjust to total invested effort
            progress = (progress[0], progress[1] + 1, progress[2], progress[3])

            thisEfforts = np.clip((np.array(tr) * amplifiers) + bases, 0.0, totalTime)
            sumThisEfforts = np.sum(thisEfforts)
            if sumThisEfforts > 0.0001:
                # adjust that sum of effort is equal total effort time
                thisEfforts = thisEfforts * totalTime / sumThisEfforts
                thisProb = computeOverallProbabilityOfDetection(allAreas, sweepWidth, velocity, thisEfforts)

                if thisProb > maxProbability:
                    maxProbability = thisProb
                    bestEfforts = thisEfforts
                    print("New best trial: ", maxProbability, bestEfforts)

            prog = math.floor(progress[1] / progress[0] * 100)
            if prog > progress[3]:
                progress = (progress[0], progress[1], progress[2], prog)
                print("Progress: ", prog, "%")

        # adjust base to best solution
        bases = bestEfforts

    # print results
    print("\n\n############## Optimal Search Strategy ##############\n" )
    print("Probability of Detection =", maxProbability * 100, "% in", totalTime/3600, "hours\n")
    for areai, ti in zip(allAreas, bestEfforts):
        print(areai[0], areai[1], ": Effort = ", ti, "s (", ti/3600, "h,", ti /totalTime*100, "% )")







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