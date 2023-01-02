from typing import Union, Iterable

import numpy as np
from numpy import ndarray

from eclipses import get_eclipses
from noise_filtering import remove_lower_extremes, remove_low_noise
from eda.plot_eclipse_hists import plot_eclipse_hists
from utils.set_dir_to_root import set_dir_to_root


def remove_doubles(eclipses, col, offset_attempts=21, bin_cnt=100):

    binwidth = 0.12  # TODO This number is coarse, fine tuning required

    no_bins = int((eclipses[col].max() - eclipses[col].min()) / binwidth)
    if no_bins < 4:
        return False, eclipses  # Your data is super "tight" already, this is useless

    no_bins = max(no_bins, 20)
    binwidth = (eclipses[col].max() - eclipses[col].min()) / no_bins  # This is the real binwidth

    # We just try offsets in spacing of 1/21 of the binwidth
    offsets = np.arange(offset_attempts) * binwidth / (offset_attempts - 1)

    results = np.zeros((offset_attempts, no_bins + 1))
    scores = np.zeros((offset_attempts, 1))

    for i, offset in enumerate(offsets):
        print(offset)
        counts, edges = np.histogram(eclipses[col], bins=no_bins + 1,
                                     range=(eclipses[col].min() - offset, eclipses[col].max() - offset + binwidth))
        # The +1s that appear here are so that the offset does not lead to eclipses being dropped
        score = np.sum(np.square(counts), axis=0)
        results[i, :] = counts
        scores[i] = score

    one_hot = (scores == np.max(scores)).astype(int).T  # which offsets maximised score?
    inverted = np.argwhere(one_hot)[:, 1]  # inverting the above
    offset = offsets[inverted[len(inverted)//2]]  # among all the offsets that maximised score, get the middle one

    counts, edges = np.histogram(eclipses[col], bins=no_bins + 1,
                                 range=(eclipses[col].min() - offset, eclipses[col].max() - offset + binwidth))
    # Recalculating because caching really is not worth the effort

    idxs = np.argsort(counts)

    combine = (False, None, None, None)  # Tuple storing if you combine or not, and which two to combine, what into

    for i, j in ((0, 1), (0, 2), (1, 2)):
        first = idxs[i]
        second = idxs[j]

        # Note that counts[first] is always bigger than counts[second]
        if abs(first - second) > 1 and (counts[first] < counts[second] * 2):
            # If they are not adjacent, and
            third = first + second
            if counts[third] > sum(counts) / 50 or counts[first] < counts[second] * 1.3:
                # If the third has a significant presence, or the first and second counts are very similar

                combine = (True, first, second, third)  # The third is unused but is useful for debugging

    if combine[0]:
        primary = eclipses[col].min() + binwidth * (combine[1] + 0.5)  # Middle of the primary eclipse bin
        secondary = eclipses[col].min() + binwidth * (combine[2] + 0.5)

        eclipses["shifted"] = eclipses[col].shift(periods=-1)
        eclipses["to_sum"] = close_to(eclipses[col], primary,
                                      binwidth / 2) & close_to(eclipses["shifted"], secondary, binwidth / 2)
        eclipses["to_drop"] = close_to(eclipses["shifted"], primary,
                                       binwidth / 2) & close_to(eclipses[col], secondary, binwidth / 2)

        eclipses.loc[eclipses["to_sum"], col] = eclipses[eclipses["to_sum"]][col] + \
                                                eclipses[eclipses["to_sum"]]["shifted"]

        eclipses = eclipses[~eclipses["to_drop"]]
        eclipses = eclipses.drop(columns=["shifted", "to_sum", "to_drop"])

        return True, eclipses

    return False, eclipses  # placeholder, duh


def close_to(x, y, epsilon):
    return ((x <= y) & (y <= x + epsilon)) | ((x - epsilon <= y) & (y <= x))  # No conditionals, this runs a decent bit


if __name__ == "__main__":
    set_dir_to_root()

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")
    # system_id = all_systems[0]  # We're building this around 19, for now
    system_id = "kplr006545018.fits"

    eclipses = get_eclipses(system_id, "data/combined")
    eclipses = remove_low_noise(eclipses, "delta")
    eclipses, thresh_upper = remove_lower_extremes(eclipses, "delta")
    plot_eclipse_hists(eclipses)

    eclipses = remove_doubles(eclipses, "delta")

    if eclipses[0]:
        plot_eclipse_hists(eclipses[1])

    eclipses = eclipses[1]
