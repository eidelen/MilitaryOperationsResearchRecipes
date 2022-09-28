import math
import scipy.optimize as opt

if __name__ == "__main__":
    print("Optimal Transportation - armasuisse W+T, Adrian Schneider")
    print("#########################################################\n")

    # road distances in km [dTM, dTW, dTA,  dIM, dIW, dIA]
    c = [12, 14, 17, 14, 21, 16]

    # unknowns number of products from-to [nTM, nTW, nTA,  nIM, nIW, nIA]

    # everything transported from depot T < 22:  nTM + nTW + nTA < 22
    # everything transported from depot I < 21:  nIM + nIW + nIA < 21
    AUb = [[1, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 1]]
    # available in depots
    qT = 22
    qI = 21
    bUb = [qT, qI]

    # demands at destinations
    # everything received by M: nTM + nIM = 15
    # everything received by W: nTW + nIW = 20
    # everything received by A: nTA + nIA = 5
    AEq = [[1, 0, 0, 1, 0, 0],
          [0, 1, 0, 0, 1, 0],
          [0, 0, 1, 0, 0, 1]]
    bEq = [15, 20, 5]

    # bounds: all n >= 0, all nTX < qT, all nMX < qI
    xBounds = [(0, qT), (0, qT), (0, qT), (0, qI), (0, qI), (0, qI)]

    res = opt.linprog(c, A_ub=AUb, b_ub=bUb, A_eq=AEq, b_eq=bEq, bounds=xBounds)

    print("Total km driven:", res.fun)
    print("Number of systems from-to:", res.x)
