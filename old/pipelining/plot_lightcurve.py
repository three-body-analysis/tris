from astropy.table import Table
import matplotlib.pyplot as plt
import wotan
import numpy as np
from old.src.eclipses import get_threshold, get_eclipses
from old.src.noise_filtering import get_filtered_and_unfiltered
from old.utils.set_dir_to_root import set_dir_to_root


def plot_curves(filename, data_path):
    table = Table.read(data_path + "/" + filename, format="fits")

    times = table["TIME"]
    sap_fluxes = table["SAP_FLUX"]

    flattened_lc = wotan.flatten(times, sap_fluxes, window_length=0.5, method='biweight')
    median = np.nanmedian(flattened_lc)
    std = np.nanstd(flattened_lc)
    threshold = get_threshold(median, std)

    fig, ax = plt.subplots(figsize=(19.2, 10.8))

    ax.plot(times, flattened_lc, '-k', label='Detrended Flux')
    ax.plot(plt.axis()[:2], [threshold, threshold], "-b", linewidth=3)

    ax.set_title('Detrended Light Curve')
    ax.legend()
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Detrended Flux (electrons/second)')

    # plt.figure(figsize=(19.2, 10.8))

    # plt.hist(flattened_lc, label="Histogram of normalised intensity")
    # plt.show()
    return fig, ax


if __name__ == "__main__":
    set_dir_to_root()

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    system_id = all_systems[11]
    # 19 is the funny high variability one, 4 is the fuzzy one
    # 9 looks like a friggin yak but I think that's fine
    # Ok looking at 10, we need a way to exclude extremely short period binaries, if they also have low variation
    # because there is no way to investigate these things, you can't even find the eclipses by eye sometimes
    # Maybe if we just detect very few eclipses we give up and mark the system as difficult, i.e. for a human

    # If we detect actually zero eclipses, or like 1-2, we can also make it try setting the threshold to like,
    # 1 std below the median instead. If that gives us a sane pattern, we can flag it tentatively

    # If it doesn't work the first time, try a threshold of 1.2 sigma. "Work" meaning get a low std on the mod plot, alongside retaining at least 50% of points (weighted)
    print(system_id)
    fig, ax = plot_curves(system_id, "data/combined")
    eclipses = get_eclipses(system_id, "data/combined")
    fig2, ax2, fig3, ax3, _ = get_filtered_and_unfiltered(eclipses)
    fig.show()
    fig2.show()
    fig3.show()
