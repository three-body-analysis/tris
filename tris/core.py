# tris/core.py
import numpy as np

from tris.io import read
from tris.preproc import detrend
from tris.eclipses import find_eclipse_timings
from tris.filter import complete_filter
from tris.oc import get_oc
from tris.periodic import remove_periodic_noise

__all__ = ["complete_pipeline"]


def complete_pipeline(filepath: str, return_plot=True):

    df_master = read(filepath)
    df = detrend(df_master)
    timings, threshold = find_eclipse_timings(df)

    if isinstance(timings, bool):
        return False, False, False, False, False

    timings = complete_filter(timings)
    oc, period = get_oc(timings)

    oc_ft_filtered = False
    oc_ft_filtered_temp = False
    if oc.shape[0] > 30:
        oc_ft_filtered = remove_periodic_noise(oc.copy(), cull_only_year=False)
    # fig and ax are null if return_plot is false
    oc, fig, ax = remove_periodic_noise(oc, cull_only_year=True, return_plot=return_plot)

    iterations = 0
    while np.mean(np.abs(oc.residuals)) > 200 / 24 / 60 and iterations < 4:
        iterations = iterations + 1
        timings, threshold_temp = find_eclipse_timings(df_master, leniency=iterations)

        if isinstance(timings, bool):
            break

        if timings.size == 0:
            break

        timings = complete_filter(timings, iterations)
        oc_temp, period_temp = get_oc(timings)
        if oc_temp.shape[0] > 30:
            oc_ft_filtered_temp = remove_periodic_noise(oc_temp.copy(), cull_only_year=False)
        oc_temp, fig_temp, ax_temp = remove_periodic_noise(oc_temp, cull_only_year=True, return_plot=return_plot)

        # Stop it from culling until there is nothing left
        if oc_temp.shape[0] < 9 or np.mean(np.abs(oc["residuals"])) * 1.2 < np.mean(np.abs(oc_temp["residuals"])):
            break
        else:
            oc = oc_temp
            threshold = threshold_temp
            oc_ft_filtered = oc_ft_filtered_temp
            period = period_temp
            fig = fig_temp
            ax = ax_temp

    return oc, oc_ft_filtered, period, iterations, threshold, fig, ax
