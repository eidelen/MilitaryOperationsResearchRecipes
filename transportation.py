import math
import scipy.optimize as opt

if __name__ == "__main__":
    print("Optimal Transportation - armasuisse W+T, Adrian Schneider")
    print("#########################################################\n")

    # (base, destination, time)

    # example https://www.youtube.com/watch?v=WZIyL6pcItY

    # unknowns [xb1, xb2, xb3, xt1, xt2, xt3]

    # costs on road[b1, b2, b3, t1, t2, t3]
    c = [5, 6, 4, 6, 3, 7]

    AUb = [[1, 1, 1, 0, 0, 0], # total number at base 1
         [0, 0, 0, 1, 1, 1]] # total number at base 2
    bUb = [900, 500]

    AEq = [[1, 0, 0, 1, 0, 0], # total delivery at dest 1
          [0, 1, 0, 0, 1, 0], # total delivery at dest 2
          [0, 0, 1, 0, 0, 1]] # total delivery at dest 3
    bEq = [200, 300, 250]

    xBounds = [(0, 300), (0, 300), (0, 300), (0, 500), (0, 500), (0, 500)]

    res = opt.linprog(c, A_ub=AUb, b_ub=bUb, A_eq=AEq, b_eq=bEq, bounds=xBounds)

    print(res)




    """
    from scipy.optimize import linprog
c = [-1, 4]
A = [[-3, 1], [1, 2]]
b = [6, 4]
x0_bounds = (None, None)
x1_bounds = (-3, None)
res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds])
res.fun
"""
