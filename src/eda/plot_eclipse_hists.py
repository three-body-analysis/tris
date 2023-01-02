import numpy as np
import matplotlib.pyplot as plt


def plot_eclipse_hists(eclipses, dims=(19.2, 10.8), offset_attempts=21, col="delta",):
    fig, ax = plt.subplots(figsize=dims)

    binwidth = 0.12
    no_bins = int((eclipses[col].max() - eclipses[col].min()) / binwidth)

    no_bins = max(no_bins, 20)
    binwidth = (eclipses[col].max() - eclipses[col].min()) / no_bins  # This is the real binwidth

    # We just try offsets in spacing of 1/21 of the binwidth
    offsets = np.arange(offset_attempts) * binwidth / (offset_attempts - 1)

    results = np.zeros((offset_attempts, no_bins + 1))
    scores = np.zeros((offset_attempts, 1))

    for i, offset in enumerate(offsets):
        counts, edges = np.histogram(eclipses[col], bins=no_bins + 1,
                                     range=(eclipses[col].min() - offset, eclipses[col].max() - offset + binwidth))
        # The +1s that appear here are so that the offset does not lead to eclipses being dropped
        score = np.sum(np.square(counts), axis=0)
        results[i, :] = counts
        scores[i] = score

    one_hot = (scores == np.max(scores)).astype(int).T  # which offsets maximised score?
    inverted = np.argwhere(one_hot)[:, 1]  # inverting the above
    offset = offsets[inverted[len(inverted) // 2]]  # among all the offsets that maximised score, get the middle one

    counts, edges = np.histogram(eclipses[col], bins=no_bins + 1,
                                 range=(eclipses[col].min() - offset, eclipses[col].max() - offset + binwidth))

    ax.hist(eclipses["delta"], bins=edges)

    return fig, ax
