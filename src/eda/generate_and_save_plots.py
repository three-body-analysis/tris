import matplotlib.pyplot as plt
import warnings
from astropy.utils.exceptions import AstropyWarning

from plot_lightcurve import plot_curves
from src.eclipses import get_eclipses
from src.noise_filtering import get_filtered_and_unfiltered
from utils.set_dir_to_root import set_dir_to_root

if __name__ == "__main__":
    set_dir_to_root()

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    plotted_systems = all_systems[:100]

    # TODO if something breaks, remove this bit and see what it is
    warnings.filterwarnings('ignore', category=AstropyWarning, append=True)

    for i in range(len(plotted_systems)):
        print("Processing Number " + str(i))

        fig1, ax1 = plot_curves(plotted_systems[i], "data/combined")
        eclipses = get_eclipses(plotted_systems[i], "data/combined")
        fig2, ax2, fig3, ax3, diagnostics = get_filtered_and_unfiltered(eclipses)
        fig1.savefig(f"generated/fluxes/{i}_flux", dpi=fig1.dpi, bbox_inches="tight")
        fig2.savefig(f"generated/deltas/{i}_deltas_raw", dpi=fig1.dpi, bbox_inches="tight")
        fig3.savefig(f"generated/deltas/{i}_deltas_filtered", dpi=fig1.dpi, bbox_inches="tight")
        print(diagnostics)
        plt.close("all")
