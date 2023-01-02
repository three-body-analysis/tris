import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from typing import List, Union, Tuple

from src.handle_double_eclipses import remove_doubles


def remove_low_noise(eclipses, col, return_dropped=False):
    # Always, always, always do this first
    threshold = 0.25
    percentile_75 = np.nanpercentile(eclipses[col], 75)

    mask = eclipses[col] > percentile_75 * threshold
    mask: np.ndarray[bool]  # to stop a stupid warning

    if return_dropped:
        return eclipses[mask], (~mask).sum()

    print((~mask).sum(), "eclipses dropped by crude noise filter")
    return eclipses[mask]


def remove_lower_extremes(eclipses, col, return_dropped=False):
    std = stats.mstats.trimmed_std(eclipses[col])
    # Here, the trimmed std is used to get the std of the central 80%, because
    # otherwise outliers skew the data to include themselves
    median = np.nanmedian(eclipses[col])

    thresh_lower = median - 5 * std
    thresh_upper = median + 5 * std

    mask = (eclipses[col] > thresh_lower)
    mask: np.ndarray[bool]  # to stop a stupid warning
    if return_dropped:
        return eclipses[mask], (~mask).sum(), thresh_upper

    print((~mask).sum(), "eclipses dropped by extreme lower filter")
    return eclipses[mask], thresh_upper


def remove_upper_extremes(eclipses, col, thresh_upper, return_dropped=False):
    # Run this only after running both remove lower extremes
    # and also handle double eclipses
    mask = (eclipses[col] < thresh_upper)
    mask: np.ndarray[bool]  # to stop a stupid warning
    if return_dropped:
        return eclipses[mask], (~mask).sum()

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


def complete_filter(eclipses, col, return_diagnositics=True)\
        -> Union[pd.DataFrame, Tuple[pd.DataFrame, Tuple[int, int, bool, int, int, bool]]]:
    # Yes, this stuff is confusing enough that I'm adding type hints
    diagnostics = [0, 0, False, 0, 0, 0, False]

    eclipses: pd.DataFrame

    if return_diagnositics:
        eclipses, diagnostics[0] = remove_low_noise(eclipses, col, return_dropped=True)
        eclipses, diagnostics[1], thresh_upper = remove_lower_extremes(eclipses, col, return_dropped=True)
        eclipses, diagnostics[2] = remove_doubles(eclipses, col, return_handling_happened=True)
        eclipses, diagnostics[3] = remove_upper_extremes(eclipses, col, thresh_upper, return_dropped=True)
        # TODO the int and bool at the end are for the KDE detection one, unfinished

        diagnostics = tuple(diagnostics)  # Exclusively for typing reasons
        diagnostics: Tuple[int, int, bool, int, int, bool]

        return eclipses, diagnostics

    # Yes I know this else is unnecessary, but it's neater
    else:
        eclipses = remove_low_noise(eclipses, col, return_dropped=False)
        eclipses, thresh_upper = remove_lower_extremes(eclipses, col, return_dropped=False)
        eclipses = remove_doubles(eclipses, col, return_handling_happened=False)
        eclipses = remove_upper_extremes(eclipses, col, thresh_upper, return_dropped=False)

        return eclipses
