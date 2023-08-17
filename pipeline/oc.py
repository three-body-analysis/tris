# pipeline/oc.py
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from pipeline.util import align_data

__all__ = [
    "estimate_constant_period",
    "distance_metric",
    "period_search",
    "get_oc"
]


def estimate_constant_period(timings):
    """Estimates the period and offset from eclipse timings

    Args:
        timings (1D Array of floats): A list of eclipse TOMS

    Returns:
        period: The estimated period (P_est)
        offset: The estimated offset (T_0)
    """

    X = np.arange(len(timings)).reshape((-1, 1))
    y = timings

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    mse = mean_squared_error(y_test, regressor.predict(X_test))

    return regressor.coef_[0], regressor.intercept_


def distance_metric(dist, spans):
    medians = np.median(dist, axis=0)
    distances = np.divide(np.abs(dist - medians), spans)
    return np.sum(distances, axis=0)


def period_search(time: pd.Series, delta: pd.Series) -> float:
    """
    Iterative gird search to identify the period.
    """
    # Median Difference between Eclipses
    initial_guess = delta.median()
    guess = initial_guess
    data = align_data(time, guess / 2)

    change = 0.1
    no_probes = 101
    max_dim = len(time)

    time = np.expand_dims(time, 1)

    best = guess
    bestval = distance_metric(data % guess, guess)
    count = 0

    while change > 1e4:
        probes = np.linspace(guess - guess * change, guess + guess * change, no_probes)
        results = np.mod(np.broadcast_to(data, (max_dim, no_probes)), probes)

        distances = distance_metric(results, probes)

        seed = np.argmin(distances)
        if distances[seed] < bestval:
            best = probes[seed]
            bestval = distances[seed]

        if seed < no_probes // 2:
            guess -= guess * change / 2
        elif seed > no_probes // 2:
            guess += guess * change / 2

        change *= 0.8
        count += 1

    best = best * round(initial_guess / best, 0)

    probes = np.linspace(best - 0.0002, best + 0.0002, no_probes)
    results = np.mod(np.broadcast_to(data, (max_dim, no_probes)), probes)

    distances = distance_metric(results, probes)

    seed = np.argmin(distances)
    if distances[seed] < bestval:
        best = probes[seed]

    return best


def get_oc(df: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    period = period_search(df.time, df.delta)
    period *= round(df.delta.median() / period, 0)
    df["residuals"] = align_data(df.time, period / 2) % period - period / 2
    return df, period
