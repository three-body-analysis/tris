# tris/preproc.py

import pandas as pd
import wotan

__all__ = [
    "detrend"
]


def detrend(df, window_length: float = 0.5, method: str = "biweight") -> pd.DataFrame:
    out = df.copy()
    out.flux = wotan.flatten(df.time, df.flux, window_length=window_length, method=method)
    return out
