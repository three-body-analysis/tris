# pipeline/core.py

from pipeline.preproc import read, detrend
from pipeline.eclipses import find_eclipse_timings
from pipeline.filter import complete_filter
from pipeline.oc import get_oc
from pipeline.periodic import remove_periodic_noise

__all__ = ["ideal_pipeline"]


def ideal_pipeline(filepath: str):
    df = detrend(read(filepath))
    df = detrend(df)
    timings = find_eclipse_timings(df)
    timings, diagnostics = complete_filter(timings, return_diagnostics=True)
    timings, period = get_oc(timings)
    timings = remove_periodic_noise(timings)
    return timings, period, diagnostics
