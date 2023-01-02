import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import seaborn as sns
from typing import List, Union, Tuple

from src.eclipses import get_eclipses, plot_eclipse_timings
from src.eda.plot_eclipse_hists import plot_eclipse_hists
from src.handle_double_eclipses import remove_doubles
from src.plotting import plot_curves
from utils.set_dir_to_root import set_dir_to_root
from src.noise_filtering import complete_filter


set_dir_to_root()
sns.set_style("whitegrid")

with open("data/all_systems.txt") as f:
    all_systems = f.read().split(",")

system_id = all_systems[0]
eclipses = get_eclipses(system_id, "data/combined")

plot_eclipse_hists(eclipses)


filtered, diagnostics = complete_filter(eclipses, "delta", return_diagnositics=True)

print(diagnostics)
plot_eclipse_hists(filtered)
plot_eclipse_timings(eclipses)
plot_eclipse_timings(filtered)

sns.kdeplot(data=eclipses, x="delta", bw_adjust=0.2)
