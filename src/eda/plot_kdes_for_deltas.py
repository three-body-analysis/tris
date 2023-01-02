import matplotlib.pyplot as plt
import warnings

import numpy as np
from astropy.utils.exceptions import AstropyWarning

from src.eclipses import get_eclipses
from src.noise_filtering import remove_low_noise, remove_extremes

import statsmodels.api as sm

from src.utils.set_dir_to_root import set_dir_to_root

threshold = 0.1

if __name__ == "__main__":
    set_dir_to_root()

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    plotted_systems = all_systems[:10]

    # TODO if something breaks, remove this bit and see what it is
    warnings.filterwarnings('ignore', category=AstropyWarning, append=True)

    for i in range(len(plotted_systems)):
        print("\nProcessing Number " + str(i))
        eclipses = get_eclipses(plotted_systems[i], "data/combined")

        half_filtered = remove_low_noise(eclipses, "delta")
        half_filtered = remove_extremes(half_filtered, "delta")

        dens = sm.nonparametric.KDEUnivariate(half_filtered["delta"])
        dens.fit(adjust=0.2)  # 0.2 or 0.3
        x = np.arange(0, half_filtered["delta"].max() + 2.5, 0.05)  # restrict range to (0,1)
        y = dens.evaluate(x)  # TODO FIX THIS WHEN I WAKE UP VERY BAD
        # TODO ALSO NOTE TURNS OUT KDE FILTERING BREAKS WHEN YOU HIT THE TELESCOPE RESOLUTION
        # TODO NO IDEA WHY

        fig, ax = plt.subplots(figsize=(19.2, 10.8))
        ax.plot(x, y)
        ax.plot(plt.axis()[:2], [threshold, threshold], "-b", linewidth=3)

        fig.savefig(f"generated/kde/{i}_flux", dpi=fig.dpi, bbox_inches="tight")
        plt.close("all")
