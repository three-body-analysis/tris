# tris/io.py

import pandas as pd
from astropy.table import Table
from typing import Union, Optional
from enum import Enum

__all__ = [
    "read_df", "read_fits", "read_csv", "read_json", "read_excel", "read"
]


class Read(Enum):
    DF = 1
    FITS = 2
    CSV = 3
    JSON = 4
    EXCEL = 5


def _preprocess_columns(df: pd.DataFrame, time: Union[int, str], flux: Union[int, str]) -> pd.DataFrame:
    if isinstance(time, str):
        time_col = df[time]
    else:
        time_col = df.iloc[:, time]

    if isinstance(flux, str):
        flux_col = df[flux]
    else:
        flux_col = df.iloc[:, flux]

    return pd.DataFrame({
        "time": time_col,
        "flux": flux_col
    })


def read_df(df: pd.DataFrame, time: Union[str, int] = 0, flux: Union[str, int] = 1) -> pd.DataFrame:
    df = _preprocess_columns(df, time, flux)
    df.dropna(how="any", inplace=True)
    return df


def read_fits(filepath: str, time: Union[str, int] = 0, flux: Union[str, int] = 1, **astropy_kwargs) -> pd.DataFrame:
    """Read FITS files as a DataFrame

    Args:
        filepath (str): The filepath to the FITS file
        time (str or int): The name / index of the Time column
        flux (str or int): The name / index of the Flux column

    Returns: pd.DataFrame Object with columns "time" and "flux"
    """
    # `.to_pandas()` is used to convert AstroPy Table to DataFrame
    # Cannot manually place data into a DataFrame as endianness changes
    df = Table.to_pandas(Table.read(
        filepath, format="fits", unit_parse_strict='silent', **astropy_kwargs
    ))

    df = read_df(df, time, flux)
    return df


def read_csv(filepath: str, time: Union[str, int] = 0, flux: Union[str, int] = 1, **pd_kwargs) -> pd.DataFrame:
    """Read CSV files as a DataFrame

    Args:
        filepath (str): The filepath to the CSV file
        time (str or int): The name / index of the Time column
        flux (str or int): The name / index of the Flux column

    Returns: pd.DataFrame Object with columns "time" and "flux"
    """
    df = pd.read_csv(
        filepath, **pd_kwargs
    )

    df = read_df(df, time, flux)
    return df


def read_json(filepath: str, time: Union[str, int] = 0, flux: Union[str, int] = 1, **pd_kwargs) -> pd.DataFrame:
    """Read JSON files as a DataFrame

    Args:
        filepath (str): The filepath to the JSON file
        time (str or int): The name / index of the Time column
        flux (str or int): The name / index of the Flux column

    Returns: pd.DataFrame Object with columns "time" and "flux"
    """
    df = pd.read_json(
        filepath, **pd_kwargs
    )

    df = read_df(df, time, flux)
    return df


def read_excel(
        filepath: str, time: Union[str, int] = 0, flux: Union[str, int] = 1,
        sheet: Union[str, int] = 0, **pd_kwargs) -> pd.DataFrame:
    """Read Excel files as a DataFrame

    Args:
        filepath (str): The filepath to the Excel file
        time (str or int): The name / index of the Time column
        flux (str or int): The name / index of the Flux column
        sheet (str or int): The sheet index or name

    Returns: pd.DataFrame Object with columns "time" and "flux"
    """
    df = pd.read_excel(
        filepath, sheet_name=sheet, **pd_kwargs
    )

    df = read_df(df, time, flux)
    return df


def read(
        item: Union[str, pd.DataFrame], time: Union[str, int] = 0, flux: Union[str, int] = 1,
        how: Read = Read.DF, sheet: Optional[Union[str, int]] = None, **kwargs
) -> pd.DataFrame:
    """

    Args:
        item (str or pd.DataFrame): either processes a filepath or a DataFrame
        time (str or int): The name / index of the Time column
        flux (str or int): The name / index of the Flux column
        sheet (str or int): The sheet index or name
        how (tris.io.Read): The method to read by. Options are [DF, FITS, CSV, JSON, EXCEL]
        sheet (str, int or None): The sheet to use (for the `read_excel` function)

    Returns: pd.DataFrame Object with columns "time" and "flux"
    """

    if isinstance(item, pd.DataFrame) or how == Read.DF:
        return read_df(item, time, flux)

    elif how == Read.FITS:
        return read_fits(item, time, flux, **kwargs)

    elif how == Read.CSV:
        return read_csv(item, time, flux, **kwargs)

    elif how == Read.JSON:
        return read_json(item, time, flux, **kwargs)

    elif how == Read.EXCEL:
        assert sheet is not None, "`sheet` variable should not be None."
        return read_excel(item, time, flux, sheet, **kwargs)

    raise ValueError("Unsupported Format Inserted")
