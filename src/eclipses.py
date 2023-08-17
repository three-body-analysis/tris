import matplotlib.pyplot as plt
import pandas as pd
import wotan
from astropy.table import Table


def get_threshold(median, std):
    if std < 0.0005:  # Super, super low std, it's noise
        return median - std * 3.2
    elif std < 0.002:  # Very low std, it's not noise, it's just eclipsing
        return median - std * 1.6
    elif std < 0.005:  # Middling std, high noise
        return median - std * 3.5
    elif std < 0.05:  # High std, it's too much for it to be noise
        return median - std * 1.4
    else:  # If the std is really high then cap the threshold
        return median - 0.070
        # I know this is discontinuous, but it actually works better.
        # A lot of curves with moderate deviations are just very periodic,
        # so if the threshold is too low you miss everything


def get_eclipses(filename, data_path):
    df = Table.to_pandas(Table.read(data_path + "/" + filename, format="fits"))
    # Note that you can't just shove table data into a dataframe
    # This is because the endianess changes. Use the .to_pandas() function
    df = df.dropna(how="any")
    df.columns = ("time", "flux")
    df["flux"] = wotan.flatten(
        df["time"], df["flux"], window_length=0.5, method='biweight')
    df["previous"] = df["flux"].shift(periods=1)

    threshold = get_threshold(df["flux"].median(), df["flux"].std())
    df["descending"] = (df["flux"] < threshold) & (df["previous"] > threshold)
    df["ascending"] = (df["flux"] > threshold) & (df["previous"] < threshold)

    crossings = df[df["descending"] | df["ascending"]]
    # As one may expect, "crossings" is a dataframe of all points where the light curve crosses the threshold

    if crossings.shape[0] < 20:  # Less than 10 eclipses, I'm not plotting much
        # TODO Figure out a better way to revise the threshold
        threshold = df["flux"].median() - df["flux"].std() * 1.3
        df["descending"] = (df["flux"] < threshold) & (
                df["previous"] > threshold)
        df["ascending"] = (df["flux"] > threshold) & (
                df["previous"] < threshold)

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
    eclipses["time"] = eclipses["time"] - eclipses.loc[0, "time"] + 1
    eclipses = eclipses.dropna(how="any")  # Last value will be NaN

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


def plot_eclipse_timings(eclipses, dims=(19.2, 10.8)):
    fig, ax = plt.subplots(figsize=dims)
    ax.scatter(data=eclipses, x="time", y="delta")
    return fig, ax
