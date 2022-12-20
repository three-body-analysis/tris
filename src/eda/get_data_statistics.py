from astropy.table import Table
import matplotlib.pyplot as plt
import wotan
import numpy as np
import time as t
from glob import glob
import pandas as pd
import pathlib



def generate_statistics(filename):
    global i
    i += 1
    table = Table.read(filename, format="fits")

    time = table["TIME"]
    flattened_lc = wotan.flatten(
        time, table["SAP_FLUX"], 
        window_length=0.5, method='biweight'
    )

    if i % 10 == 0:
        print("Processing number", str(i), "at", t.time() - now, "seconds...")

    return pd.Series(dict(
        mean = np.nanmean(flattened_lc),
        std = np.nanstd(flattened_lc),
        min_time = np.nanmin(time),
        max_time = np.nanmax(time)
    ))


if __name__ == "__main__":
    i = 0
    local_dir = pathlib.Path(__file__).parent
    now = t.time()
    all_systems = pd.Series(glob("data/combined/*.fits"))

    print("Storing data to", str(local_dir / "statistics.csv"))
    print("Readings:", len(all_systems))

    all_systems.apply(generate_statistics).to_csv(
        str(local_dir / "statistics.csv"), index=False)
