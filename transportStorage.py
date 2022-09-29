import scipy.optimize as opt

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Optimal Transportation and Storage - armasuisse W+T, Adrian Schneider")
    print("#####################################################################\n")

    airTransportCostPerShell = 10       # airlifts at day 2, day 3 and day 4
    truckTransportCostPerShell = 5      # road transport at day 1
    storageFrontCostsPerShell = 4

    truckCapacity = 4000
    airLiftCapacity = 1500

    useShellsDay1, useShellsDay2, useShellsDay3, useShellsDay4 = 1000, 2500, 500, 2000

    # unknowns to solve:
    # [shellDeliverDay1, ..., shellDeliverDay4, shellStorageDay1, ..., shellStorageDay4]

    # objective cost function to minimize in respect to unknowns
    #        truck transport day 1        air lift day 2            air lift day 3            truck transport day 4
    costs = [truckTransportCostPerShell, airTransportCostPerShell, airTransportCostPerShell, airTransportCostPerShell,
    #        storage day 1              storage day 2              storage day 3              storage day 4
             storageFrontCostsPerShell, storageFrontCostsPerShell, storageFrontCostsPerShell, storageFrontCostsPerShell]


    AEq = [
              # connecting shell delivery, shell usage and shell storage in respect to order of unknowns
              [1, 0, 0, 0,   -1, 0, 0, 0],  # shellDeliverDay1 - shellStorageDay1 = useShellsDay1
              [0, 1, 0, 0,    1, -1, 0, 0], # shellDeliverDay2 + shellStorageDay1 - shellStorageDay2 = useShellsDay2
              [0, 0, 1, 0,    0, 1, -1, 0],  # shellDeliverDay3 + shellStorageDay2 - shellStorageDay3 = useShellsDay3
              [0, 0, 0, 1,    0, 0, 1, -1],  # shellDeliverDay4 + shellStorageDay3 - shellStorageDay4 = useShellsDay4
          ]
    bEq = [useShellsDay1, useShellsDay2, useShellsDay3, useShellsDay4]


    AUb = [
                [1, 0, 0, 0,   0, 0, 0, 0],  # shellDeliverDay1 <= truckCapacity
                [0, 1, 0, 0,   0, 0, 0, 0],  # shellDeliverDay2 <= airLiftCapacity
                [0, 0, 1, 0,   0, 0, 0, 0],  # shellDeliverDay3 <= airLiftCapacity
                [0, 0, 0, 1,   0, 0, 0, 0],  # shellDeliverDay4 <= airLiftCapacity
          ]
    bUb = [truckCapacity, airLiftCapacity, airLiftCapacity, airLiftCapacity]


    res = opt.linprog(costs, A_eq=AEq, b_eq=bEq, A_ub=AUb, b_ub=bUb)

    print("Total costs:", res.fun)
    print("Transports [road, air, air , air]:", res.x)



    r = np.arange(4)
    width = 0.25
    plt.bar(r, (res.x)[:4], color='b', width=width, edgecolor='black', label='Delivery')
    plt.bar(r + width, [useShellsDay1, useShellsDay2, useShellsDay3, useShellsDay4], color='g', width=width, edgecolor='black', label='Demand')
    plt.bar(r + 2*width, (res.x)[4:], color='r', width=width, edgecolor='black', label='Stock')

    plt.axhline(y=truckCapacity, linewidth=2, color='black', label='Truck Capacity')
    plt.axhline(y=airLiftCapacity, linewidth=2, color='grey', label='Air Lift Capacity')

    plt.ylabel("Number of Shells")
    plt.title("Transport & Storage Optimization")
    plt.xticks(r + width, ['Day 1 (Road)', 'Day 2 (Air)', 'Day 3 (Air)', 'Day 4 (Air)'])
    plt.legend()
    plt.show()
