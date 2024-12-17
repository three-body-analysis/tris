# tris/periodic.py
import numpy as np
import pandas as pd
from scipy.fftpack import rfft, irfft, fftfreq
import matplotlib.pyplot as plt

__all__ = [
    "remove_periodic_noise"
]

from typing import Union, Tuple, Any


def remove_periodic_noise(df: pd.DataFrame, cull_only_year = True, return_plot = False) -> Union[pd.DataFrame, Tuple[pd.DataFrame, Any, Any]]:
    y = df.residuals.values - df.residuals.mean()

    N = len(y)
    T = df.time.max() / N

    f_signal = rfft(y)
    W = fftfreq(y.size, d=T)

    if return_plot:
        fig, ax = plt.subplots()
        ax.plot(W[:N // 2], 2.0 / N * np.abs(f_signal[:N // 2]))

    # filter out frequencies with periods of about a year
    f_signal[((abs(W) > 0.0025) & (abs(W) < 0.0030))] = 0
    if not cull_only_year:
        # filter out frequencies with periods less than 10 days
        f_signal[(abs(W) > 0.1)] = 0
    # due to wrap-around
    f_signal[(W < 0)] = 0

    culled_residuals = irfft(f_signal)
    df.loc[:, "residuals"] = culled_residuals

    if return_plot:
        return df, fig, ax

    return df
