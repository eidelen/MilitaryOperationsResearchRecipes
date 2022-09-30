import unittest
import scipy.optimize as opt

class TestLinearProgrammingTricks(unittest.TestCase):

    def test_simple_LP(self):
        # Problem described https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
        # Minimize objective function = -x0 + 4x1
        # Constraint 1) -3x0 + x1 <= 6   -> 2d: y <= 6 + 3x
        # Constraint 2) -x0 - 2x1 >= -4  -> 2d: y >= 2 - 0.5x
        # Constraint 3) x1 >= -3  -> 2d: y >= 3

        # scipy only supports <=, thus Constr. 2) 3) has to be reformulated
        # Constraint 2) -x0 - 2x1 >= -4 -> x0 + 2x1 <= 4
        # Constraint 3) x1 >= -3 -> -x1 <= 3

        objFunc = [-1, 4]

        ALessEq = [
                        [-3, 1], # Constraint 1) -3x0 + x1 <= 6
                        [1, 2],  # Constraint 2) x0 + 2x1 <= 4
                        [0, -1]  # Constraint 3)  -x1 <= 3
                  ]
        bLessEq = [6, 4, 3]

        # The value range x0 and x1 can take.
        # IMPORTANT!!!! Default range is x >= 0. That is why in this example we explicitly state no bounds.
        # Note: Constraint 3) could be specified via bound as well
        theBounds = [(None, None), (None, None)]

        res = opt.linprog(c=objFunc, A_ub=ALessEq, b_ub=bLessEq, bounds=theBounds)

        self.assertAlmostEqual(res.fun, -22.0)
        self.assertAlmostEqual(res.x[0], 10)
        self.assertAlmostEqual(res.x[1], -3)


if __name__ == '__main__':
    unittest.main()