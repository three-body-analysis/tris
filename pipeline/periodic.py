# pipeline/periodic.py
import pandas as pd
from scipy.fftpack import rfft, irfft, fftfreq

__all__ = [
    "remove_periodic_noise"
]


def remove_periodic_noise(df: pd.DataFrame) -> pd.DataFrame:
    y = df.residuals.values - df.residuals.mean()

    N = len(y)
    T = df.time.max() / N

    f_signal = rfft(y)
    W = fftfreq(y.size, d=T)

    # filter out frequencies with periods of about a year
    f_signal[((abs(W) > 0.0025) & (abs(W) < 0.003))] = 0
    # filter out frequencies with periods less than 20 days
    f_signal[(abs(W) > 0.05)] = 0
    # due to wrap-around
    f_signal[(W < 0)] = 0

    culled_residuals = irfft(f_signal)
    df["culled_residuals"] = culled_residuals
    return df
