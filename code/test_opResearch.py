import unittest
import localization
import math
import numpy as np

class TestOperationsReseachRecipes(unittest.TestCase):

    def test_localization_distance(self):
        # line: y = x same for y = -x
        # test points on line -> zero dist
        for i in np.linspace(-10.0, 10.0, num=200):
            dist = localization.dist_pnt2line((math.pi / 4, (0.0, 0.0)), (i, i) )
            self.assertAlmostEqual(dist, 0.0)
            dist = localization.dist_pnt2line((math.pi / 4 + math.pi, (0.0, 0.0)), (i, i))
            self.assertAlmostEqual(dist, 0.0)


if __name__ == '__main__':
    unittest.main()