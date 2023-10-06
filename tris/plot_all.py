import warnings

import matplotlib.pyplot as plt
import numpy as np
import wotan
from astropy.utils.exceptions import AstropyWarning
from astropy.table import Table

from tris import ideal_pipeline, compute_threshold


def plot_and_export_lightcurve(kic):
    df = Table.read(f"../data/combined/{kic}.fits", format="fits") # not using read() because of speed

    times = df["TIME"]

    df = wotan.flatten(times, df["SAP_FLUX"], window_length=0.5, method='biweight')
    # not using detrend() because it relies on some relabeling done by read()

    times = times - times.min()
    median = np.nanmedian(df)
    std = np.nanstd(df)
    threshold = compute_threshold(median, std)

    fig, ax = plt.subplots(figsize=(12.8, 7.2))

    ax.plot(times, df, '-k', label='Detrended Flux')
    ax.plot(plt.axis()[:2], [threshold, threshold], "-b", linewidth=3)

    ax.set_title('Detrended Light Curve')
    ax.legend()
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Detrended Flux (electrons/second)')

    fig.savefig(f"../generated/fluxes/{i}_flux", dpi=fig.dpi, bbox_inches="tight")

def plot_and_export_cpoc(kic):

    oc, _ = ideal_pipeline(f"../data/combined/{kic}.fits")
    oc["min_res"] = oc.residuals * 24 * 60
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(
        x=oc["time"], y=oc["min_res"], s=50
    )
    ax.set_xlabel("Time / days")
    ax.set_ylabel("O-C / min")

    fig.savefig(f"../generated/cpoc/{i}_cpoc", dpi=fig.dpi, bbox_inches="tight")

if __name__ == "__main__":

    with open("../data/all_systems.txt") as f:
        all_systems = f.read().split("\n")

    # with open("data/cpop_diagnostics.txt", "w") as out:
    #    out.write("noise,outliers,doubles,density\n")

    start = 0
    end = 2865

    # TODO if something breaks, remove this bit and see what it is
    warnings.filterwarnings('ignore', category=AstropyWarning, append=True)

    for i in range(start, end + 1):
        if i % 10 == 0:
            print("\nProcessing Number " + str(i))
            plt.close("all")

        print(all_systems[i])

        plot_and_export_cpoc(all_systems[i])
        plot_and_export_lightcurve(all_systems[i])