import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from typing import List, Union, Tuple
import wquantiles

from src.handle_double_eclipses import remove_doubles


def remove_low_noise(eclipses, col, return_dropped=False):
    # Always, always, always do this first
    threshold = 0.25
    percentile_75 = wquantiles.quantile(eclipses[col], eclipses[col], 0.75)

    mask: np.ndarray[bool] = eclipses[col] > percentile_75 * threshold
    if np.mean(eclipses[col]) > 0.3:
        mask = mask & (eclipses[col] > 0.1) # drop the garbage

    if return_dropped:
        return eclipses[mask], (~mask).sum()

    print((~mask).sum(), "eclipses dropped by low noise filter")
    return eclipses[mask]


def remove_high_noise(eclipses, col, return_dropped=False):
    # Only ever do this if remove_low_noise was not called BUT the weighted percentile was high-ish
    threshold = 4
    median = np.nanmedian(eclipses[col])

    mask: np.ndarray[bool] = eclipses[col] < median * threshold

    if return_dropped:
        return eclipses[mask], -(~mask).sum()

    print((~mask).sum(), "eclipses dropped by high noise filter")
    return eclipses[mask]


def remove_outliers(eclipses, col, return_dropped=False, sigma=5):
    std = stats.mstats.trimmed_std(eclipses[col])
    # Here, the trimmed std is used to get the std of the central 80%, because
    # otherwise outliers skew the data to include themselves
    median = np.nanmedian(eclipses[col])

    thresh_lower = median - sigma * std
    thresh_upper = median + sigma * std

    mask = (eclipses[col] > thresh_lower) & (eclipses[col] < thresh_upper)
    mask: np.ndarray[bool]  # to stop a stupid warning
    if return_dropped:
        return eclipses[mask], (~mask).sum()

    print((~mask).sum(), "eclipses dropped by outlier filter")
    return eclipses[mask]


def get_filtered_and_unfiltered(eclipses):
    fig1, ax1 = plt.subplots(figsize=(19.2, 10.8))
    ax1.scatter(data=eclipses, x="time", y="delta", label="Unfiltered")

    eclipses, diagnostics = complete_filter(eclipses, "delta", return_diagnositics=True)
    # Gets the trimmed std (central 80%) and drops all points that have deltas more than 5 sigma from the median

    fig2, ax2 = plt.subplots(figsize=(19.2, 10.8))
    ax2.scatter(data=eclipses, x="time", y="delta", label="Filtered")
    return fig1, ax1, fig2, ax2, diagnostics


def complete_filter(eclipses, col, return_diagnositics=True)\
        -> Union[pd.DataFrame, Tuple[pd.DataFrame, Tuple[int, int, bool, int, bool]]]:
    # Yes, this stuff is confusing enough that I'm adding type hints
    diagnostics: List = [0, 0, False, 0, False]

    eclipses: pd.DataFrame

    if return_diagnositics:
        if wquantiles.quantile(eclipses[col], eclipses[col], 0.75) > 1 and stats.mstats.trimmed_std(eclipses["delta"]) > 0.7:
            eclipses, diagnostics[0] = remove_low_noise(eclipses, col, return_dropped=True)
        elif wquantiles.quantile(eclipses[col], eclipses[col], 0.75) > 1:
            eclipses, diagnostics[0] = remove_high_noise(eclipses, col, return_dropped=True)
        eclipses, diagnostics[1] = remove_outliers(eclipses, col, return_dropped=True)
        eclipses, diagnostics[2] = remove_doubles(eclipses, col, return_handling_happened=True)
        # TODO the int and bool at the end are for the KDE detection one, unfinished

        diagnostics: Tuple[int, int, bool, int, bool] = tuple(diagnostics)  # Exclusively for typing reasons

        eclipses = eclipses.reset_index(drop=True)

        return eclipses, diagnostics

    # Yes I know this else is unnecessary, but it's neater
    else:
        if wquantiles.quantile(eclipses[col], eclipses[col], 0.75) > 1 and stats.mstats.trimmed_std(eclipses["delta"]) > 0.7:
            eclipses = remove_low_noise(eclipses, col, return_dropped=False)
        elif wquantiles.quantile(eclipses[col], eclipses[col], 0.75) > 1:
            eclipses = remove_high_noise(eclipses, col, return_dropped=False)
        eclipses = remove_outliers(eclipses, col, return_dropped=False)
        eclipses = remove_doubles(eclipses, col, return_handling_happened=False)

        eclipses = eclipses.reset_index(drop=True)

        return eclipses
