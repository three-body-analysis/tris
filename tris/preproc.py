# tris/preproc.py

import pandas as pd
from astropy.table import Table
import wotan

__all__ = [
    "read", "detrend"
]


def read(filepath: str) -> pd.DataFrame:
    # `.to_pandas()` is used to convert AstroPy Table to DataFrame
    # Cannot manually place data into a DataFrame as endianness changes
    df = Table.to_pandas(Table.read(filepath, format="fits"))
    df.dropna(how="any", inplace=True)
    df.columns = ("time", "flux")
    return df


def detrend(df, window_length: float = 0.5, method: str = "biweight") -> pd.DataFrame:
    df.flux = wotan.flatten(df.time, df.flux, window_length=window_length, method=method)
    return df
