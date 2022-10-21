import unittest
import numpy as np
from hmmlearn import hmm

class TestHiddenMarkovModels(unittest.TestCase):

    def test_simple_hmm(self):
        randomSeed = 5

        simpleModel = hmm.CategoricalHMM(n_components=2, random_state=randomSeed)

        # state 1 at start
        simpleModel.startprob_ = np.array([0.0, 1.0])

        # model always ends in state 1
        simpleModel.transmat_ = np.array([[0.0, 1.0],    # being in state 0, it always changes in state 1
                                        [0.0, 1.0]])   # state 1 stays in state 1

        # state 1 always activates output 0
        simpleModel.emissionprob_ = np.array([[1.0, 0.0], [0.0, 1.0]])

        samples, corrStates = simpleModel.sample(4)

        np.testing.assert_array_equal(samples, [[1], [1], [1], [1]])
        np.testing.assert_array_equal(corrStates, [1, 1, 1, 1])


    def test_hmm_score(self):

        # strictly alternating states

        # starts in state 0
        startStateProb = np.array([1.0, 0.0, 0.0])

        stateTransMat = np.array([
            [0.0, 1.0, 0.0],  # state 0 to state 1
            [0.0, 0.0, 1.0],  # state 1 to state 2
            [1.0, 0.0, 0.0]   # state 2 to state 0
        ])

        stateEmissionProb = np.array([
            [1.0, 0.0, 0.0],  # state 0 -> obs 0
            [0.0, 1.0, 0.0],  # state 1 -> obs 1
            [0.0, 0.0, 1.0]   # state 2 -> obs 2
        ])

        # init hmm
        myHmm = hmm.CategoricalHMM(n_components=3, random_state=10)
        myHmm.startprob_ = startStateProb
        myHmm.transmat_ = stateTransMat
        myHmm.emissionprob_ = stateEmissionProb

        # sample the hmm: always 0, 1, 2, 0, 1, 2, 0 ...
        nSamples = 9
        obsStates, _ = myHmm.sample(nSamples)
        np.testing.assert_array_equal(obsStates, [[0], [1], [2], [0], [1], [2], [0], [1], [2]])

        # check how likely observation is

        # perfect
        self.assertAlmostEqual(myHmm.score(np.array([[0, 1, 2]])), 0.0, 0.00001)
        self.assertAlmostEqual(myHmm.score(np.array([[0, 1, 2, 0]])), 0.0, 0.00001)

        # impossible
        self.assertLess(myHmm.score(np.array([[0, 0, 1]])), -1000000)
        self.assertLess(myHmm.score(np.array([[1, 2, 0]])), -1000000)

