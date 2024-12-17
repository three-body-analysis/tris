# tris/__init__.py

from tris.io import read, read_df, read_fits, read_csv, read_json, read_excel
from tris.preproc import detrend
from tris.eclipses import compute_threshold, compute_crossings, find_eclipse_timings
from tris.filter import denoise_mask, outlier_filter_mask, double_filter_mask, complete_filter
from tris.oc import distance_metric, period_search, get_oc
from tris.periodic import remove_periodic_noise
from tris.core import complete_pipeline

__all__ = [
    "read", "read_df", "read_fits", "read_csv", "read_json", "read_excel",
    "detrend",
    "compute_threshold", "compute_crossings", "find_eclipse_timings",
    "denoise_mask", "outlier_filter_mask", "double_filter_mask", "complete_filter",
    "distance_metric", "period_search", "get_oc",
    "remove_periodic_noise",
    "complete_pipeline"
]
