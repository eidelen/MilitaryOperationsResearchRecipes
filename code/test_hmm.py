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

