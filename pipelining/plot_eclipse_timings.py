from src.eclipses import get_eclipses, plot_eclipse_timings

if __name__ == "__main__":

    with open("data/all_systems.txt") as f:
        all_systems = f.read().split(",")

    system_id = all_systems[4]
    # We're building this around 19, for now
    # Wow number 10 is awful

    # Number 11 is funny, like there's a line outside the main region that just gets dropped by remove_extremes

    # system_id = "kplr006545018.fits"  # Override when convenient
    fig1, ax1, fig2, ax2 = plot_eclipse_timings(get_eclipses(system_id, "data/combined"))
    fig1.show()
    fig2.show()

