from astropy.table import Table
from scipy import stats
import matplotlib.pyplot as plt
import wotan
import numpy as np
import pandas as pd
import warnings
from astropy.utils.exceptions import AstropyWarning

from plot_lightcurve import plot_curves
from plot_eclipse_timings import get_eclipses, plot_eclipse_timings

with open("data/all_systems.txt") as f:
    all_systems = f.read().split(",")

plotted_systems = all_systems[:100]

# TODO if something breaks, remove this bit and see what it is
warnings.filterwarnings('ignore', category=AstropyWarning, append=True)

for i in range(len(plotted_systems)):
    print("Processing Number " + str(i))

    fig1, ax1 = plot_curves(plotted_systems[i], "data/combined")
    eclipses = get_eclipses(plotted_systems[i], "data/combined")
    fig2, ax2, fig3, ax3 = plot_eclipse_timings(eclipses)
    fig1.savefig(f"generated_images/{i}_flux", dpi=fig1.dpi, bbox_inches="tight")
    fig2.savefig(f"generated_images/{i}_deltas_raw", dpi=fig1.dpi, bbox_inches="tight")
    fig3.savefig(f"generated_images/{i}_deltas_trimmed", dpi=fig1.dpi, bbox_inches="tight")
    plt.close("all")
