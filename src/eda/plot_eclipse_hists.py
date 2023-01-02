import numpy as np
import matplotlib.pyplot as plt


def plot_eclipse_hists(eclipses):
    binwidth = 0.15  # TODO This number is totally arbitrary, fine tuning required
    no_bins = int((eclipses["delta"].max() - eclipses["delta"].min()) / binwidth)
    no_bins = max(no_bins, 20)
    binwidth = (eclipses["delta"].max() - eclipses["delta"].min()) / no_bins  # This is the real binwidth

    plt.hist(eclipses["delta"], bins=no_bins)
    plt.xticks(np.linspace(round(eclipses["delta"].min(), 2) - 0.1,
                           round(no_bins * binwidth + eclipses["delta"].min(), 2) + 0.1, 11))
    plt.show()

    counts, edges = np.histogram(eclipses["delta"], bins=no_bins)
