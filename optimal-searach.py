def doOptSearch():
    print("Optimal Search Strategy - armasuisse W+T")

    # define parameters
    w = 200  # m
    v = 10   # m/s
    t = 24 * 60 * 60 # s
    areas = [("A1", "urban", 14100000, 0.6), ("A2", "mountain", 6300000, 0.1), ("A3", "mountain", 4100000, 0.1),
             ("A4", "water", 3500000, 0.4), ("A5", "water", 1900000, 0.4), ("A6", "mountain", 9100000, 0.1)]

    print("w=" + str(w) + " m, v=" + str(v) + " m/s, t=" + str(t) + " s")
    for area_name, area_type, area_size, prop in areas:
        print(area_name + ": " + area_type + ", " + str(area_size) + " m^2, " + "p=" + str(prop))




if __name__ == "__main__":
    doOptSearch()