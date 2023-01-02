import numpy as np

from eclipses import get_eclipses
from noise_filtering import remove_extremes
from eda.plot_eclipse_hists import plot_eclipse_hists
from utils.set_dir_to_root import set_dir_to_root


def remove_doubles(eclipses, offset_attempts = 30, bin_cnt = 100):

    binwidth = (eclipses["delta"].max() - eclipses["delta"].min()) / 100  # TODO This number is totally arbitrary, fine tuning required

    # We just try offsets in spacing of 1/30 of the binwidth
    for offset in np.arange(offset_attempts) * binwidth / (offset_attempts - 1):

        no_bins = int((eclipses["delta"].max() - eclipses["delta"].min()) / binwidth)
        if no_bins < 4:
            return False, eclipses  # Your data is super "tight" already, this is useless

        binwidth = (eclipses["delta"].max() - eclipses["delta"].min()) / no_bins  # This is the real binwidth

        counts, edges = np.histogram(eclipses["delta"], bins=max(no_bins, 20), range=(eclipses["delta"].min() - offset, eclipses["delta"].max() - offset))

        idxs = np.argsort(counts)

        combine = (False, None, None, None)  # Tuple storing if you combine or not, and which two to combine, what into

        for i, j in ((0, 1), (0, 2), (1, 2)):
            first = idxs[i]
            second = idxs[j]

            # Note that counts[first] is always bigger than counts[second]
            if abs(first - second) > 1 and (counts[first] < counts[second] * 2):
                # If they are not adjacent, and
                third = first + second
                if counts[third] > sum(counts) / 50:
                    combine = (True, first, second, third)  # The third is unused but is useful for debugging

        if combine[0]:
            primary = eclipses["delta"].min() + binwidth * (combine[1] + 0.5)  # Middle of the primary eclipse bin
            secondary = eclipses["delta"].min() + binwidth * (combine[2] + 0.5)

            eclipses["shifted"] = eclipses["delta"].shift(periods=-1)
            eclipses["to_sum"] = close_to(eclipses["delta"], primary,
                                        binwidth / 2) & close_to(eclipses["shifted"], secondary, binwidth / 2)
            eclipses["to_drop"] = close_to(eclipses["shifted"], primary,
                                        binwidth / 2) & close_to(eclipses["delta"], secondary, binwidth / 2)

            eclipses.loc[eclipses["to_sum"], "delta"] = eclipses[eclipses["to_sum"]]["delta"] + \
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
    eclipses = remove_extremes(eclipses, "delta")
    plot_eclipse_hists(eclipses)

    eclipses = remove_doubles(eclipses)

    if eclipses[0]:
        plot_eclipse_hists(eclipses[1])

    eclipses = eclipses[1]
