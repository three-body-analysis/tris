from astropy.table import Table
from scipy import stats
import matplotlib.pyplot as plt
import wotan
import numpy as np
import pandas as pd
from get_threshold import get_threshold


def remove_extremes(arr, col):
    std = stats.mstats.trimmed_std(arr[col])
    # Here, the trimmed std is used to get the std of the central 80%, because
    # otherwise outliers skew the data to include themselves
    median = np.nanmedian(arr[col])

    thresh_lower = median - 5 * std
    thresh_upper = median + 5 * std
    print(str(((arr[col] > thresh_upper) | (arr[col] < thresh_lower)).sum()) + " eclipses dropped")
    return arr[(arr[col] < thresh_upper) & (arr[col] > thresh_lower)]


def plot_eclipse_timings(eclipses):
    fig1, ax1 = plt.subplots(figsize=(19.2, 10.8))
    ax1.scatter(data=eclipses, x="time", y="delta", label="Untrimmed")

    eclipses = remove_extremes(eclipses, "delta")
    # Gets the trimmed std (central 80%) and drops all points that have deltas more than 5 sigma from the median

    fig2, ax2 = plt.subplots(figsize=(19.2, 10.8))
    ax2.scatter(data=eclipses, x="time", y="delta", label="Trimmed")
    return fig1, ax1, fig2, ax2


def get_eclipses(filename, data_path):
    df = Table.to_pandas(Table.read(data_path + "/" + filename, format="fits"))
    # Note that you can't just shove table data into a dataframe
    # This is because the endianess changes. Use the .to_pandas() function
    df = df.dropna(how="any")
    df.columns = ("time", "flux")
    df["flux"] = wotan.flatten(df["time"], df["flux"], window_length=0.5, method='biweight')
    df["previous"] = df["flux"].shift(periods=1)

    threshold = get_threshold(df["flux"].median(), df["flux"].std())
    df["descending"] = (df["flux"] < threshold) & (df["previous"] > threshold)
    df["ascending"] = (df["flux"] > threshold) & (df["previous"] < threshold)

    crossings = df[df["descending"] | df["ascending"]]
    # As one may expect, "crossings" is a dataframe of all points where the light curve crosses the threshold

    if crossings.shape[0] < 20:  # Less than 10 eclipses, I'm not plotting much
        threshold = df["flux"].median() - df["flux"].std() * 1.3  # TODO Figure out a better way to revise the threshold
        df["descending"] = (df["flux"] < threshold) & (df["previous"] > threshold)
        df["ascending"] = (df["flux"] > threshold) & (df["previous"] < threshold)

        crossings = df[df["descending"] | df["ascending"]]

    if crossings.iloc[0, 4]:
        crossings = crossings[1:]
        # An eclipse has to start from somewhere, so if the first entry is the end of an eclipse, ignore it

    crossings.reset_index(drop=False, inplace=True)

    eclipses = pd.DataFrame()
    eclipses["time"] = crossings["time"].rolling(
        window=pd.api.indexers.FixedForwardWindowIndexer(window_size=2)).mean()[::2]
    eclipses["duration"] = (crossings["time"].shift(periods=-1) - crossings["time"])[::2]
    eclipses["delta"] = eclipses["time"].shift(periods=-1) - eclipses["time"]

    # the eclipse time is the average of the "start" and "stop" crossings,
    # the duration is less important but is the difference,
    # and the delta is the time until the next eclipse

    # For now, this is just a plot for my brain to process. Soon, there should be actual analysis.
    # But for now, this is just there for eyeballing

    # TODO Find a way to get rid of clusters on the delta against time curve,
    #  since those happen when the threshold is too lenient and noise gets through. Look at system [1], for example

    # Maybe I take like, the 80th percentile delta, and discard any data point that's like, 10 times shorter than it?
    # Unfortunately that also means that if we have one erroneous spike,
    # we discard both the spike and the datapoint after it, hmm

    return eclipses


if __name__ == "__main__":

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    system_id = all_systems[4]
    # We're building this around 19, for now
    # Wow number 10 is awful

    # Number 11 is funny, like there's a line outside the main region that just gets dropped by remove_extremes

    # system_id = "kplr006545018.fits"  # Override when convenient
    fig1, ax1, fig2, ax2 = plot_eclipse_timings(get_eclipses(system_id, "data/combined"))
    fig1.show()
    fig2.show()

