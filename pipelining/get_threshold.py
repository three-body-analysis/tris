def get_threshold(median, std):
    if std < 0.005:
        return median - std * 3
    elif std < 0.05:
        return median - std * 1.4
        # I know this is discontinuous, but it actually works better.
        # A lot of curves with moderate deviations are just very periodic,
        # so if the threshold is too low you miss everything
    else:
        return median - 0.070  # Change this last bit