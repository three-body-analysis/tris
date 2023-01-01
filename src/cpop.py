import numpy as np
from numpy.fft import *
from scipy.stats import stats
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics


def estimateConstantPeriod(timings):
    """Estimates the period and offset from eclipse timings

    Args:
        timings (1D Array of floats): A list of eclipse TOMS

    Returns:
        period: The estimated period (P_est)
        offset: The estimated offset (T_0)
    """

    # Its just a simple linear regression on the timings
    x_train, x_test, y_train, y_test = train_test_split(np.arange(len(timings)).reshape((-1, 1)), timings, test_size=0.2, random_state=0)

    regressor = LinearRegression()
    regressor.fit(x_train, y_train)  # training the algorithm

    # Print the error of estimation
    print("MSE of estimation", metrics.mean_squared_error(y_test, regressor.predict(x_test)))
    return regressor.coef_[0], regressor.intercept_


def distance_metric(dist, spans):
    medians = np.median(dist, axis=0)
    distances = np.divide(np.abs(dist - medians), spans)
    return np.sum(distances, axis=0)


def period_stupid_search(data, deltas):
    # Ok this took a lot of tinkering, but it kinda works? I tried smarter searches but they were unreliable
    # It's basically just an iterative grid search
    # TODO: Do more tinkering to see what the general minimum required computation for convergence is

    # The initial guess should be the median difference between eclipses
    # I still need to figure out how to handle systems with weird phases for secondary eclipses
    guess = deltas.median()
    data = align_data(data, guess / 2)

    change = max(round(guess / 10, 1), 0.1) / guess
    no_probes = 51
    max_dim = len(data)
    data = np.expand_dims(data, 1)

    best = guess
    bestval = distance_metric(data % guess, guess)

    count = 0
    while count < 100 and change > 1e-8:
        probes = np.linspace(guess - guess * change, guess + guess * change, no_probes)
        results = np.mod(np.broadcast_to(data, (max_dim, no_probes)), probes)

        distances = distance_metric(results, probes)

        seed = np.argmin(distances)
        if distances[seed] < bestval:
            best = probes[seed]
            bestval = distances[seed]

        if seed < no_probes // 2:
            guess = guess - change / 2
        elif seed > no_probes // 2:
            guess = guess + change / 2
        change = change * 3 / 4
        count = count + 1
    return best


def align_data(data, new_offset):
    return data - data[0] + new_offset


def remove_extremes(arr):
    std = stats.mstats.trimmed_std(arr)
    # Here, the trimmed std is used to get the std of the central 80%, because
    # otherwise outliers skew the data to include themselves
    median = np.nanmedian(arr)

    thresh_lower = median - 5 * std
    thresh_upper = median + 5 * std
    print(str(((arr > thresh_upper) | (arr < thresh_lower)).sum()) + " eclipses dropped")
    return arr[(arr < thresh_upper) & (arr > thresh_lower)]


def getOC(eclipses, author="Vikram", n_periods = 2):
    """Using estimated period and offset, get the O-C values

    Args:
        eclipses: Pandas DataFrame containing eclipse timings, duration, and delta (time till previous eclipse)
        author: The person who coded out the period searching function

    Returns:
        O-C: An array of floats, representing the O-C values
    """
    
    if author == "Vikram":
        period = period_stupid_search(eclipses['time'], eclipses['delta'].median())
        offset = (eclipses['time'] % period).median()
    elif author == "Yuan Xi":
        period, offset = estimateConstantPeriod(eclipses['time'])

    if n_periods == 2:
        period2 = fftfreq(eclipses['time'].size)[np.argmax(fft(eclipses['time'] % period - offset)[1:])]
        return (eclipses['time'] % period - offset) % period2 - ((eclipses['time'] % period - offset) % period2).mean()

    # return eclipses['time'] - offset - np.arange(len(eclipses['time'])) * period
    return eclipses['time'] % period - offset