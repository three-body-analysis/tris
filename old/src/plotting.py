import matplotlib.pyplot as plt
import numpy as np
import wotan
from astropy.table import Table

from old.src.eclipses import get_threshold
from old.utils.set_dir_to_root import set_dir_to_root


def plot_curves(filename):
    table = Table.read(filename, format="fits")

    times = table["TIME"]
    sap_fluxes = table["SAP_FLUX"]

    flattened_lc = wotan.flatten(times, sap_fluxes, window_length=0.5, method='biweight')

    times = times - times.min()
    median = np.nanmedian(flattened_lc)
    std = np.nanstd(flattened_lc)
    threshold = get_threshold(median, std)

    fig, ax = plt.subplots(figsize=(12.8, 7.2))

    ax.plot(times[:600], flattened_lc[:600], '-k', label='Detrended Flux')
    ax.plot(plt.axis()[:2], [threshold, threshold], "-b", linewidth=3)

    ax.set_title('Detrended Light Curve')
    ax.legend()
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Detrended Flux (electrons/second)')

    return fig, ax


if __name__ == "__main__":
    set_dir_to_root()

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    system_id = all_systems[181]
    print(system_id)
    fig, ax = plot_curves("data/combined/" + system_id)
    fig.show()
