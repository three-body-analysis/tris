from typing import Union, Tuple, Any

import pandas as pd

__all__ = [
    "compute_threshold",
    "compute_crossings",
    "find_eclipse_timings"
]

from pandas import DataFrame


def compute_threshold(median: float, std: float, leniency: int) -> float:
    lenient_mod = 1 + leniency * 0.8

    if std < 0.0005:
        # Incredibly low std --> Noise
        return median - std * 3.2 * lenient_mod
    elif std < 0.001:
        # Very low std --> eclipsing dangerously close to noise
        return median - std * 2.4 * lenient_mod
    elif std < 0.002:
        # Quite low std --> eclipsing (not noise)
        return median - std * 1.6 * lenient_mod
    elif std < 0.005:
        # Middling std --> high noise
        return median - std * 3.5 * lenient_mod
    elif std < 0.05:
        # High std --> too much for just noise
        return median - std * 1.4 * lenient_mod
    else:
        # Incredibly high std
        # Threshold has been capped
        # a lot of curves with moderate deviations are very periodic
        return median - 0.070


def compute_crossings(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    previous = df.flux.shift(periods=1)

    ascending = (df.flux >= threshold) & (previous < threshold)
    descending = (df.flux <= threshold) & (previous > threshold)

    crossings = df[ascending | descending]

    if ascending.sum():
        if crossings.iloc[0].time == df[ascending].iloc[0].time:
            # An eclipse has to start with a descending node, so if the crossings
            # start with an ascending node, the ascending node needs to be culled.
            crossings = crossings.iloc[1:]

    crossings = crossings.reset_index(drop=True)

    new_crossings = []

    working_pair_1 = 0
    for i in range(1, len(crossings)):
        if working_pair_1 is not None and crossings.time[i] - crossings.time[working_pair_1] < 0.3:
            new_crossings.append(working_pair_1)
            new_crossings.append(i)
            working_pair_1 = None
        else:
            working_pair_1 = i

    crossings = crossings.iloc[new_crossings]
    return crossings


def find_eclipse_timings(df: pd.DataFrame, leniency : int = 0) -> Tuple[DataFrame, Union[float, Any]]:
    threshold = compute_threshold(df.flux.median(), df.flux.std(), leniency)
    crossings = compute_crossings(df, threshold)

    if crossings.shape[0] < 20:
        # Less than 20 eclipses, so we do it again
        threshold = df.flux.median() - df.flux.std() * 1.3
        crossings_2 = compute_crossings(df, threshold)
        if crossings_2.size > crossings.size:
            crossings = crossings_2

    if crossings.shape[0] < 5:
        # Less than 5 eclipses, so we do it again
        threshold = df.flux.median() - df.flux.std() * 1.1
        crossings_2 = compute_crossings(df, threshold)
        if crossings_2.size > crossings.size:
            crossings = crossings_2

    crossings.reset_index(drop=False)

    assert crossings.time.values.shape[0] % 2 == 0

    if crossings.size == 0:
        return False, threshold

    pairs = crossings.time.values.reshape(-1, 2)

    eclipses = pd.DataFrame()
    # compute the average of the "start" and "stop" crossing
    eclipses["time"] = pairs.mean(axis=1)
    # compute the duration of the eclipse
    eclipses["duration"] = pairs[:, 1] - pairs[:, 0]
    # compute difference between eclipse times (ETVs)
    eclipses["delta"] = eclipses.time.shift(periods=-1) - eclipses.time
    # now we reset the time to start from time "1"
    eclipses.time += 1 - eclipses.loc[0, "time"]

    # Last value will be NaN
    eclipses.dropna(how="any", inplace=True)

    return eclipses, threshold


