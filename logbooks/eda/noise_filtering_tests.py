import numpy as np
import seaborn as sns
import statsmodels.api as sm
from matplotlib import pyplot as plt

from src.eclipses import get_eclipses, plot_eclipse_timings
from logbooks.eda.plot_eclipse_hists import plot_eclipse_hists
from src.noise_filtering import complete_filter
from utils.set_dir_to_root import set_dir_to_root

set_dir_to_root()
sns.set_style("whitegrid")

with open("data/all_systems.txt") as f:
    all_systems = f.read().split(",")

system_id = all_systems[13]  # 44
eclipses = get_eclipses(system_id, "data/combined")

plot_eclipse_hists(eclipses)

filtered, diagnostics = complete_filter(eclipses, "delta", return_diagnositics=True)

print(diagnostics)
fig1, ax1 = plot_eclipse_hists(eclipses)
fig1.show()
fig2, ax2 = plot_eclipse_hists(filtered)
fig2.show()
fig3, ax3 = plot_eclipse_timings(eclipses)
fig3.show()
fig4, ax4 = plot_eclipse_timings(filtered)
fig4.show()

plt.cla()
dens = sm.nonparametric.KDEUnivariate(filtered["delta"])
dens.fit(adjust=0.25)  # 0.2 or 0.3
x = np.linspace(0, filtered["delta"].max() * 1.1, 1000)
y = dens.evaluate(x) * x

fig, ax = plt.subplots(figsize=(19.2, 10.8))
ax.plot(x, y)
# ax.plot(plt.axis()[:2], [threshold, threshold], "-b", linewidth=3)

fig.show()
