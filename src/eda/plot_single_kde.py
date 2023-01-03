import matplotlib.pyplot as plt
import warnings

import numpy as np
from astropy.utils.exceptions import AstropyWarning

from src.eclipses import get_eclipses
from src.noise_filtering import complete_filter

import statsmodels.api as sm

from utils.set_dir_to_root import set_dir_to_root

if __name__ == "__main__":
    set_dir_to_root()

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")
    i = 98

    # TODO if something breaks, remove this bit and see what it is
    warnings.filterwarnings('ignore', category=AstropyWarning, append=True)

    print("\nProcessing Number " + str(i))
    eclipses = get_eclipses(all_systems[i], "data/combined")

    filtered, diagnostics = complete_filter(eclipses, "delta", return_diagnositics=True)

    dens = sm.nonparametric.KDEUnivariate(filtered["delta"])
    dens.fit(adjust=0.2)  # 0.2 or 0.3
    x = np.linspace(0, filtered["delta"].max() * 1.1, 500)
    y = dens.evaluate(x) * x

    fig, ax = plt.subplots(figsize=(19.2, 10.8))
    ax.plot(x, y)
    # ax.plot(plt.axis()[:2], [threshold, threshold], "-b", linewidth=3)

    fig.show()
    print(diagnostics)
