from scipy.fftpack import rfft, irfft, fftfreq


def cull_oscillations(eclipses, col):
    y = eclipses[col].values - eclipses[col].mean()

    # oversampled_amount = int(math.pow(2, math.ceil(math.log(len(y),2))) - len(y))
    # if oversampled_amount / len(y) < 0.2:
    #    y = np.pad(y, (0, oversampled_amount), mode='constant')

    N = len(y)
    T = eclipses["time"].max() / N

    f_signal = rfft(y)
    W = fftfreq(y.size, d=T)

    culled_f_signal = f_signal.copy()
    culled_f_signal[((abs(W) > 0.0025) & (abs(W) < 0.003))] = 0  # filter out frequencies with periods of about a year
    culled_f_signal[(abs(W) > 0.05)] = 0  # filter out frequencies with periods less than 20 days
    culled_f_signal[(W < 0)] = 0  # because wrap-around is a thing
    culled_signal = irfft(culled_f_signal)
    eclipses["culled_" + col] = culled_signal
    return eclipses
