# tris/core.py

from tris.io import read
from tris.preproc import detrend
from tris.eclipses import find_eclipse_timings
from tris.filter import complete_filter
from tris.oc import get_oc
from tris.periodic import remove_periodic_noise

__all__ = ["ideal_pipeline"]


def ideal_pipeline(filepath: str):
    df = read(filepath)
    df = detrend(df)
    timings = find_eclipse_timings(df)
    timings = complete_filter(timings)
    oc, period = get_oc(timings)
    oc = remove_periodic_noise(oc)
    return oc, period
