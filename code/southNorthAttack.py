from hmmlearn import hmm

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("South North Attack HMM - armasuisse W+T, Adrian Schneider")
    print("#########################################################\n")

    # initialization of random seed: guarantees repeatability of experiment
    randomSeed = 28

    # first state probability: Fog   Cloud  Sun
    startStateProb = np.array([1/3,  1/3,   1/3])

    # state transition probability matrix:   Fog   Cloud   Sun
    stateTransMat = np.array(   [
                                 #   Fog   Cloud  Sun
                                    [0.3,  0.4,   0.3], # transitions from state fog
                                    [0.2,  0.5,   0.3], # transitions from state cloud
                                    [0.2,  0.2,   0.6]  # transitions from state sun
                                ] )

    stateEmissionProb = np.array(   [
                                     #   North     South
                                        [0.4,      0.6],     # attacking side when fog
                                        [0.2,      0.8],    # attacking side when cloud
                                        [0.8,      0.2]      # attacking side when sun
                                    ])

    # init hmm
    attackHMM = hmm.CategoricalHMM( n_components=3, random_state=randomSeed )
    attackHMM.startprob_ = startStateProb
    attackHMM.transmat_ = stateTransMat
    attackHMM.emissionprob_ = stateEmissionProb


    # sample the hmm and create attacking statistics
    nSamples = 100000
    attackSides, hiddenStates = attackHMM.sample(nSamples)
    northProb = np.count_nonzero(attackSides == 0) / nSamples
    southProb = np.count_nonzero(attackSides == 1) / nSamples

    print("Sampling HMM n=", nSamples)
    print("North Attack Probability:", northProb)
    print("South Attack Probability:", southProb)

    cntAtks = [[0, 0, 0], [0, 0, 0]]
    for ats, hs in zip(attackSides, hiddenStates):
        cntAtks[ats[0]][hs] += 1

    # predict next days' attack side based on last 12 days observation
    # note: documentation is somehow bad
    nextDayNorthLogProb = np.array([[0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0,       0]])
    nextDaySouthLogProb = np.array([[0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0,       1]])

    print("Likely attack tomorrow:")
    print("North:", attackHMM.score(nextDayNorthLogProb))
    print("South:", attackHMM.score(nextDaySouthLogProb))


    nBars = 2
    fogCnts = (cntAtks[0][0], cntAtks[1][0])
    cloudCnts = (cntAtks[0][1], cntAtks[1][1])
    sunCnts = (cntAtks[0][2], cntAtks[1][2])
    basePlotSun = (cntAtks[0][0]+cntAtks[0][1], cntAtks[1][0]+cntAtks[1][1])
    ind = np.arange(2)  # the x locations for the groups
    width = 0.25
    plt.bar(ind, fogCnts, width, color='r')
    plt.bar(ind, cloudCnts, width, bottom=fogCnts, color='b')
    plt.bar(ind, sunCnts, width, bottom=basePlotSun, color='g')
    plt.ylabel('Counts')
    plt.xlabel('Attack Side')
    plt.title('Attack Side by Reason (n=' + str(nSamples) + ')')
    plt.xticks(ind, ('North', 'South'))
    plt.legend(labels=['Foggy', 'Cloudy', 'Sunny'])
    plt.show()
