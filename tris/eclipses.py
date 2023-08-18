import pandas as pd

__all__ = [
    "compute_threshold",
    "compute_crossings",
    "find_eclipse_timings"
]


def compute_threshold(median: float, std: float) -> float:
    if std < 0.0005:
        # Incredibly low std --> Noise
        return median - std * 3.2
    elif std < 0.002:
        # Very low std --> eclipsing (not noise)
        return median - std * 1.6
    elif std < 0.005:
        # Middling std --> high noise
        return median - std * 3.5
    elif std < 0.05:
        # High std --> too much for just noise
        return median - std * 1.4
    else:
        # Incredibly high std
        # Threshold has been capped
        # a lot of curves with moderate deviations are very periodic
        return median - 0.070


def compute_crossings(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    previous = df.flux.shift(periods=1)

    descending = (df.flux < threshold) & (previous > threshold)
    ascending = (df.flux > threshold) & (previous < threshold)

    crossings = df[descending | ascending]

    if ascending.sum():
        if crossings.iloc[0].time == df[ascending].iloc[0].time:
            # An eclipse has to start with a descending node, so if the crossings
            # start with an ascending node, the ascending node needs to be culled.
            crossings = crossings.iloc[1:]

    if descending.sum():
        if crossings.iloc[-1].time == df[descending].iloc[-1].time:
            # Cull any eclipses that aren't completed
            crossings = crossings.iloc[:-1]

    return crossings


def find_eclipse_timings(df: pd.DataFrame) -> pd.DataFrame:
    threshold = compute_threshold(df.flux.median(), df.flux.std())
    crossings = compute_crossings(df, threshold)

    if crossings.shape[0] < 20:
        # Less than 10 eclipses, so we do again
        threshold = df.flux.median() - df.flux.std() * 1.3
        crossings = compute_crossings(df, threshold)

    crossings.reset_index(drop=False)

    assert crossings.time.values.shape[0] % 2 == 0

    pairs = crossings.time.values.reshape(-1, 2)

    eclipses = pd.DataFrame()
    # compute the average of the "start" and "stop" crossing
    eclipses["time"] = pairs.mean(axis=1)
    # compute the duration of the eclipse
    eclipses["duration"] = pairs[:, 1] - pairs[:, 0]
    # compute difference between eclipse times (ETVs)
    eclipses["delta"] = eclipses.time.shift(periods=-1) - eclipses.time
    # now we reset the time to start from time "1"
    eclipses.time += 1-eclipses.loc[0, "time"]

    # Last value will be NaN
    eclipses.dropna(how="any", inplace=True)

    return eclipses


