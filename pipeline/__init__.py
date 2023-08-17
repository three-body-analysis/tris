# pipeline/__init__.py

from pipeline.preproc import read, detrend
from pipeline.eclipses import compute_threshold, compute_crossings, find_eclipse_timings
from pipeline.filter import denoise_mask, outlier_filter_mask, double_filter_mask, complete_filter
from pipeline.oc import distance_metric, period_search, get_oc
from pipeline.periodic import remove_periodic_noise
from pipeline.core import ideal_pipeline

__all__ = [
    "read", "detrend", "compute_threshold", "compute_crossings", "find_eclipse_timings",
    "denoise_mask", "outlier_filter_mask", "double_filter_mask", "complete_filter",
    "distance_metric", "period_search", "get_oc", "remove_periodic_noise", "ideal_pipeline"
]
