# tris/filter.py
import pandas as pd
import wquantiles
from scipy import stats
import numpy as np
from typing import Tuple, Union

from tris.util import close_to

__all__ = [
    "denoise_mask", "outlier_filter_mask",
    "double_filter_mask",
    "complete_filter"
]


def denoise_mask(delta: Union[pd.Series, np.ndarray]) -> np.ndarray:
    percentile_75 = wquantiles.quantile(delta, delta, 0.75)
    std = stats.mstats.trimmed_std(delta)

    if percentile_75 > 1 and std > 0.7:
        threshold = 0.25
        mask: np.ndarray = delta > (percentile_75 * threshold)

        if delta.mean() > 0.3:
            # drop "garbage"
            mask &= delta > 0.1

        return mask

    elif percentile_75 > 1:
        threshold = 4
        median = np.nanmedian(delta)
        return delta < (median * threshold)

    else:
        return np.ones_like(delta, dtype=bool)


def outlier_filter_mask(delta: pd.Series, sigma: float = 5) -> np.ndarray:
    # Here, the trimmed std is used to get the std of the central 80%
    # otherwise outliers skew the data to include themselves
    std = stats.mstats.trimmed_std(delta)
    median = np.nanmedian(delta)

    thresh_lower = median - sigma * std
    thresh_upper = median + sigma * std

    mask: np.ndarray = (delta > thresh_lower) & (delta < thresh_upper)

    if mask.sum() == 0:
        mask = mask | (~mask)

    return mask


def double_filter_mask(delta, offset_attempts: int = 21) -> Tuple[np.ndarray, np.ndarray, bool]:
    # offset_attempts should be an odd number

    delta_range = delta.max() - delta.min()

    binwidth = 0.12

    no_bins = int(delta_range / binwidth)

    if no_bins < 4:
        # Data is very "tight", no need to remove doubles
        return np.zeros_like(delta), np.ones_like(delta, dtype=bool), False

    no_bins = max(no_bins, 20)
    # Real binwidth
    binwidth = delta_range / no_bins

    # We try offsets in the spacing of 1/offset_attempts of the binwidth
    offsets = np.arange(offset_attempts) * binwidth / (offset_attempts - 1)

    results = np.zeros((offset_attempts, no_bins + 1))

    for i, offset in enumerate(offsets):
        counts, edges = np.histogram(
            delta, bins=no_bins + 1,
            range=(delta.min() - offset, delta.max() - offset + binwidth)
        )

        # +1 is used so that offset does not lead to eclipses being dropped
        results[i, :] = counts

    scores = np.sum(np.square(results), axis=1)

    # get the middle offset that maximises score
    inverted = np.where(scores == np.max(scores))[0]
    offset = offsets[inverted[inverted.shape[0] // 2]]

    counts, edges = np.histogram(
        delta, bins=no_bins + 1,
        range=(delta.min() - offset, delta.max() - offset + binwidth)
    )

    idxs = np.argsort(counts)[::-1]

    for i, j in ((0, 1), (0, 2), (1, 2)):
        first, second = idxs[i], idxs[j]

        # note that counts[first] > counts[second]

        if abs(first - second) > 1 and (counts[first] < counts[second] * 2.5) and not (
                close_to(first * 2, second, binwidth * 2) or close_to(first, second * 2, binwidth * 2)):
            # if they are not adjacent, and are reasonably close together
            # But they aren't close to being doubles of one another
            # third = first + second

            primary = delta.min() + binwidth * (first + 0.5)
            secondary = delta.min() + binwidth * (second + 0.5)

            shifted = delta.shift(periods=-1)
            to_sum = close_to(delta, primary, binwidth * 1.5) & close_to(delta, secondary, binwidth * 1.5)
            to_drop = close_to(shifted, primary, binwidth * 1.5) & close_to(delta, secondary, binwidth * 1.5)

            shifted[~to_sum] = 0
            mask = ~to_drop

            return shifted, mask, True

        return np.zeros_like(delta), np.ones_like(delta, dtype=bool), False


def complete_filter(eclipses: pd.DataFrame, return_diagnostics=False) -> Union[
    pd.DataFrame, Tuple[pd.DataFrame, Tuple[Union[int, bool]]]]:
    diagnostics = []

    denoiser = denoise_mask(eclipses.delta)
    eclipses = eclipses[denoiser]
    diagnostics.append(int((~denoiser).sum()))

    outlier_filter = outlier_filter_mask(eclipses.delta)
    eclipses = eclipses[outlier_filter]
    diagnostics.append(int((~outlier_filter).sum()))

    to_add, double_filter, handling_happened = double_filter_mask(eclipses.delta)
    eclipses.delta += to_add
    eclipses: pd.DataFrame = eclipses[double_filter]
    diagnostics.append(handling_happened)
    diagnostics.append(int((~double_filter).sum()))

    eclipses.reset_index(drop=True, inplace=True)

    if return_diagnostics:
        return eclipses, tuple(diagnostics)
    else:
        return eclipses
