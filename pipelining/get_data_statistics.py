from astropy.table import Table
import matplotlib.pyplot as plt
import wotan
import numpy as np
import time as t


data = []  # "data" stores a tuple of (mean, deviation, min_x, max_x)

with open("data/all_systems.txt", "r") as f:
    all_systems = f.read().split(",")

print(len(all_systems))
now = t.time()

for i in range(len(all_systems)):
    table = Table.read("data/combined/" + all_systems[i], format="fits")

    time = table["TIME"]
    flattened_lc = wotan.flatten(time, table["SAP_FLUX"], window_length=0.5, method='biweight')

    data.append((
        np.nanmean(flattened_lc),
        np.nanstd(flattened_lc),
        np.nanmin(time),
        np.nanmax(time)
    ))
    if i % 10 == 0:
        print("\nProcessing number " + str(i))
        print(t.time() - now)

print(data)

with open("statistics.csv", "w") as stats:
    for quad in data:
        stats.write(str(quad[0]) + "," + str(quad[1]) + "," + str(quad[2]) + "," + str(quad[3]) + "\n")
