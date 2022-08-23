import math
import scipy.optimize as opt


def meanTimeOfDetection(sweepWidth, velocity, area):
    # meantime of detection -> denoted T in formula
    return area / (velocity * sweepWidth) # denoted T in formula

def randomSearchKoopman(sweepWidth, velocity, area, time):
    # The probability of detecting a target in given time and area
    return 1.0 - math.exp(-time/meanTimeOfDetection(sweepWidth, velocity, area))

def accumulateProbabilityOfDetection(allAreas, sweepWidth, velocity, efforts):
    # accumulates the probability of detection given search efforts
    probAccum = 0
    for ar, time in zip(allAreas, efforts):
        _, _, areaSize, areaProb = ar
        probAccum += areaProb * randomSearchKoopman(sweepWidth, velocity, areaSize, time)
    return probAccum

def minimizeAccumProbOfDetection(efforts, areas, sweepWidth, velocity):
    # function to minimize
    val = 0
    for time, ar in zip(efforts, areas):
        _, _, areaSize, prob = ar
        val += prob * math.exp(-time/meanTimeOfDetection(sweepWidth, velocity, areaSize))
    return val

def gradientMinAccumProbOfDetection(efforts, areas, sweepWidth, velocity):
    # gradient of the function to minimize
    drv = []
    for time, ar in zip(efforts, areas):
        _, _, areaSize, prob = ar
        c = meanTimeOfDetection(sweepWidth, velocity, areaSize)
        d = prob * -1.0/c * math.exp(-(time/c))
        drv.append(d)
    return drv

def solveBySLSQP(allAreas, sweepWidth, velocity, totalTime):
    # solve by using SLSQP solver with constraints
    nArea = len(allAreas)

    minFunc = lambda efforts: minimizeAccumProbOfDetection(efforts, allAreas, sweepWidth, velocity)
    gradientMinFunc = lambda efforts: gradientMinAccumProbOfDetection(efforts, allAreas, sweepWidth, velocity)

    # sum of all efforts needs to be equal the total time
    cons = ({'type': 'eq', 'fun': lambda efforts: totalTime - sum(efforts)})

    # optimizer
    print("\n------- optimizer output ----------")
    optSLSQPRes = opt.minimize(minFunc, [t for t in range(nArea)],
                               method='SLSQP',
                               options={'ftol': 1e-20, 'disp': True},
                               jac=gradientMinFunc,
                               constraints=cons,
                               bounds=[(0, totalTime) for x in range(nArea)])
    print("------------------------------------")

    # print results
    maxDetectionProb = accumulateProbabilityOfDetection(allAreas, sweepWidth, velocity, optSLSQPRes.x)
    print("\n############## Optimal Search Strategy - SLSQP Method ##############\n")
    print("Probability of Detection =", maxDetectionProb * 100, "% in", totalTime / 3600, "hours\n")
    for area, time in zip(allAreas, optSLSQPRes.x):
        print(area[0], area[1], ": Effort = ", time, "s (", time / 3600, "h,", time / totalTime * 100, "% )")

if __name__ == "__main__":
    print("Optimal Search Strategy - armasuisse W+T, Adrian Schneider")
    print("##########################################################\n")

    # define parameters
    w = 200  # m
    v = 10  # m/s
    t = 3 * 60 * 60  # s
    areas = [("A1", "urban", 14100000, 0.55), ("A2", "mountain", 6300000, 0.05), ("A3", "mountain", 4100000, 0.05),
             ("A4", "water", 3500000, 0.15), ("A5", "water", 1900000, 0.15), ("A6", "mountain", 9100000, 0.05)]

    print("w=" + str(w) + " m, v=" + str(v) + " m/s, t=" + str(t) + " s")
    for area_name, area_type, area_size, prop in areas:
        print(area_name + ": " + area_type + ", " + str(area_size) + " m^2, " + "p=" + str(prop))

    solveBySLSQP(areas, w, v, t)

    # compute non-optimized detection probability
    totalArea = 0
    for _, _, anArea, _ in areas:
        totalArea += anArea
    nonOptProb = randomSearchKoopman(w, v, totalArea, t)
    print("\nProbability of Detection non-optimized =", nonOptProb * 100, "%, total area =", totalArea / 1000000, "km^2")
