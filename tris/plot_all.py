import warnings

import matplotlib.pyplot as plt
import numpy as np
import wotan
from astropy.utils.exceptions import AstropyWarning
from astropy.table import Table
import time

from tris import complete_pipeline, compute_threshold


def plot_and_export_lightcurve(kic, threshold):
    df = Table.read(f"../data/combined/{kic}.fits", format="fits") # not using read() because of speed

    times = df["TIME"]

    df = wotan.flatten(times, df["SAP_FLUX"], window_length=0.5, method='biweight')
    # not using detrend() because it relies on some relabeling done by read()

    times = times - times.min()

    fig, ax = plt.subplots(figsize=(12.8, 7.2))

    ax.plot(times, df, '-k', label='Detrended Flux')
    ax.plot(plt.axis()[:2], [threshold, threshold], "-b", linewidth=3)

    ax.set_title('Detrended Light Curve')
    ax.legend()
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Detrended Flux')  # This is normalised and thus dimensionless

    fig.savefig(f"../generated/fluxes/{i}_flux", dpi=fig.dpi, bbox_inches="tight")

def plot_and_export_cpoc(kic):

    oc, oc_ft_filtered, _, iterations, threshold, fig, ax = complete_pipeline(f"../data/combined/{kic}.fits")
    if isinstance(oc, bool):
        return iterations

    fig.savefig(f"../generated/ft/{i}_ft", dpi=fig.dpi, bbox_inches="tight")
    plt.close(fig)

    oc["min_res"] = oc.residuals * 24 * 60

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(
        x=oc["time"], y=oc["min_res"], s=50
    )
    ax.set_xlabel("Time / days")
    ax.set_ylabel("O-C / min")

    fig.savefig(f"../generated/cpoc/{i}_cpoc", dpi=fig.dpi, bbox_inches="tight")
    plt.close(fig)

    if not isinstance(oc_ft_filtered, bool):
        oc_ft_filtered["min_res"] = oc_ft_filtered.residuals * 24 * 60
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(
            x=oc_ft_filtered["time"], y=oc_ft_filtered["min_res"], s=50
        )
        ax.set_xlabel("Time / days")
        ax.set_ylabel("O-C / min")

        fig.savefig(f"../generated/cpoc_ft_filtered/{i}_cpoc", dpi=fig.dpi, bbox_inches="tight")
        plt.close(fig)

    return iterations, threshold


start_time = time.time()

if __name__ == "__main__":

    with open("../data/all_systems.txt") as f:
        all_systems = f.read().split("\n")

    # with open("data/cpop_diagnostics.txt", "w") as out:
    #    out.write("noise,outliers,doubles,density\n")


    start = 610
    end = 2864

    # TODO if something breaks, remove this bit and see what it is
    warnings.filterwarnings('ignore', category=AstropyWarning, append=True)

    for i in range(start, end + 1):
        if i % 10 == 0:
            print("\nProcessing Number " + str(i) + " at time " + str(round(time.time() - start_time, 1)) + "s")
            plt.close("all")

        print(all_systems[i])

        iterations, threshold = plot_and_export_cpoc(all_systems[i])
        plot_and_export_lightcurve(all_systems[i], threshold)

    print("Final time: " + str(round(time.time() - start_time, 1)) + "s")