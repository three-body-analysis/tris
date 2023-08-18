import warnings

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from astropy.utils.exceptions import AstropyWarning

from src.eclipses import get_eclipses
from src.noise_filtering import complete_filter
from utils.set_dir_to_root import set_dir_to_root

if __name__ == "__main__":
    set_dir_to_root()

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    plotted_systems = all_systems[:100]

    # TODO if something breaks, remove this bit and see what it is
    warnings.filterwarnings('ignore', category=AstropyWarning, append=True)

    for i in range(len(plotted_systems)):
        print("\nProcessing Number " + str(i))
        eclipses = get_eclipses(plotted_systems[i], "data/combined")

        filtered, diagnostics = complete_filter(eclipses, "delta", return_diagnositics=True)

        dens = sm.nonparametric.KDEUnivariate(filtered["delta"])
        dens.fit(adjust=0.25)  # 0.2 to 0.3
        x = np.linspace(0, filtered["delta"].max() * 1.1, 1000)
        y = dens.evaluate(x) * x

        fig, ax = plt.subplots(figsize=(19.2, 10.8))
        ax.plot(x, y)
        # ax.plot(plt.axis()[:2], [threshold, threshold], "-b", linewidth=3)

        fig.savefig(f"generated/kde/{i}_flux", dpi=fig.dpi, bbox_inches="tight")
        plt.close("all")

        print(diagnostics)
