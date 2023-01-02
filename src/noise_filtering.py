import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import seaborn as sns

from src.eclipses import get_eclipses, plot_eclipse_timings
from src.handle_double_eclipses import remove_doubles
from utils.set_dir_to_root import set_dir_to_root


def remove_low_noise(eclipses, col):
    # Always, always, always do this first
    threshold = 0.25
    percentile_75 = np.nanpercentile(eclipses[col], 75)
    mask = eclipses[col] > percentile_75 * threshold

    print((~mask).sum(), "eclipses dropped by crude noise filter")
    return eclipses[mask]


def remove_lower_extremes(eclipses, col):
    std = stats.mstats.trimmed_std(eclipses[col])
    # Here, the trimmed std is used to get the std of the central 80%, because
    # otherwise outliers skew the data to include themselves
    median = np.nanmedian(eclipses[col])

    thresh_lower = median - 5 * std
    thresh_upper = median + 5 * std

    mask = (eclipses[col] > thresh_lower)

    print((~mask).sum(), "eclipses dropped by extreme lower filter")
    return eclipses[mask], thresh_upper


def remove_upper_extremes(eclipses, col, thresh_upper):
    # Run this only after running both remove lower extremes
    # and also handle double eclipses
    mask = (eclipses[col] < thresh_upper)
    print((~mask).sum(), "eclipses dropped by extreme upper filter")
    return eclipses[mask]


def get_filtered_and_unfiltered(eclipses):
    fig1, ax1 = plt.subplots(figsize=(19.2, 10.8))
    ax1.scatter(data=eclipses, x="time", y="delta", label="Untrimmed")

    eclipses = remove_low_noise(eclipses, "delta")
    eclipses, thresh_upper = remove_lower_extremes(eclipses, "delta")
    # Gets the trimmed std (central 80%) and drops all points that have deltas more than 5 sigma from the median

    fig2, ax2 = plt.subplots(figsize=(19.2, 10.8))
    ax2.scatter(data=eclipses, x="time", y="delta", label="Trimmed")
    return fig1, ax1, fig2, ax2


def complete_filter(eclipses, col):
    eclipses = remove_low_noise(eclipses, "delta")
    eclipses = remove_lower_extremes(eclipses, "delta")

    eclipses = remove_doubles(eclipses, "delta")


if __name__ == "__main__":
    set_dir_to_root()
    sns.set_style("whitegrid")

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    system_id = all_systems[0]

    eclipses = get_eclipses(system_id, "data/combined")
    fig1, ax1, fig2, ax2 = get_filtered_and_unfiltered(eclipses)

    fig1.show()
    fig2.show()

    sns.kdeplot(data=eclipses, x="delta", bw_adjust=0.2)
