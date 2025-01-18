# tris/oc.py
from typing import Tuple

import numpy as np
import pandas as pd

from tris import outlier_filter_mask
from tris.util import align_data

__all__ = [
    "distance_metric",
    "period_search",
    "get_oc"
]


def distance_metric(dist, periods):
    # MSE tends to compensate for outliers too heavily
    distances = np.abs(dist - periods / 2)
    return np.mean(distances, axis=0)


def period_search(initial_guess: float, time: pd.Series) -> float:
    """
    Iterative gird search to identify the period.
    """
    # Median Difference between Eclipses
    guess = initial_guess

    change = max(0.1, guess / 30)
    no_probes = 101
    max_dim = len(time)
    time = np.expand_dims(time, 1)

    best = guess
    bestval = distance_metric(time % guess, guess)

    count = 0
    while change > 0.02:
        probes = np.linspace(guess - guess * change, guess + guess * change, no_probes)
        results = np.mod(np.broadcast_to(time, (max_dim, no_probes)), probes)

        distances = distance_metric(results, probes)

        seed = np.argmin(distances)
        if distances[seed] < bestval:
            best = probes[seed]
            bestval = distances[seed]

        if seed < no_probes // 2:
            guess -= guess * change / 2
        elif seed > no_probes // 2:
            guess += guess * change / 2

        change *= 0.85
        count += 1

    best = best * round(initial_guess / best, 0)
    time = align_data(time, best / 2)

    probes = np.linspace(best - 0.02, best + 0.02, no_probes*200 + 1)
    results = np.mod(np.broadcast_to(time, (max_dim, no_probes*200 + 1)), probes)

    distances = distance_metric(results, probes)

    seed = np.argmin(distances)
    if distances[seed] < bestval:
        best = probes[seed]

    return best


def final_adjustment_for_linearity_trend(time: pd.Series, residuals: pd.Series):
    coef = np.polyfit(time, residuals, 1)
    return residuals - align_data(np.poly1d(coef)(time), 0), coef[0]


def get_oc(df: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    guess = df.loc[:, "delta"].median()
    aligned = align_data(df.loc[:, "time"], guess / 2)

    period = period_search(guess, aligned)
    # Account for accidentally converging to a higher order harmonic
    period *= round(df.delta.median() / period, 0)

    # Realign data and apply linear correction
    df.loc[:, "residuals"] = align_data(df.loc[:, "time"], period / 2) % period - period / 2
    outlier_mask = outlier_filter_mask(df.loc[:, "residuals"])
    df = df.loc[outlier_mask]

    residuals_temp, gradient = final_adjustment_for_linearity_trend(df.loc[:, "time"], df.loc[:, "residuals"])

    # If the corrected is better or close enough, take it. Else, ignore it
    if np.mean(np.abs(df.residuals)) > np.mean(np.abs(residuals_temp)) * 0.99:
        df.loc[:, "residuals"] = residuals_temp
        period = period + gradient * period

    return df, period
