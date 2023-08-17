import warnings

from astropy.utils.exceptions import AstropyWarning
from scipy import stats

from src.cpop import getOC
from src.eclipses import get_eclipses
from utils.set_dir_to_root import set_dir_to_root

if __name__ == "__main__":
    set_dir_to_root()

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    with open("data/estimates.txt", "w") as out:
        out.write("not\n")

    start = 0
    end = 2864

    # TODO if something breaks, remove this bit and see what it is
    warnings.filterwarnings('ignore', category=AstropyWarning, append=True)

    for i in range(start, end + 1):
        if i % 10 == 0:
            print("\nProcessing Number " + str(i))
        eclipses = get_eclipses(all_systems[i], "data/combined")

        eclipses, period, diagnostics = getOC(eclipses, return_diagnostics=True)
        if stats.mstats.trimmed_std(eclipses["culled_residuals"] * 1440) > 20:
            out = "1\n"
        else:
            out = "\n"

        with open("data/estimates.txt", "a") as estimates:
            estimates.write(out)
