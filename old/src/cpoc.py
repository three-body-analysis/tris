import numpy as np
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from old.src.cull_oscillations import cull_oscillations
from old.src.noise_filtering import complete_filter


def estimateConstantPeriod(timings):
    """Estimates the period and offset from eclipse timings

    Args:
        timings (1D Array of floats): A list of eclipse TOMS

    Returns:
        period: The estimated period (P_est)
        offset: The estimated offset (T_0)
    """

    # Its just a simple linear regression on the timings
    x_train, x_test, y_train, y_test = train_test_split(np.arange(len(timings)).reshape((-1, 1)), timings,
                                                        test_size=0.2, random_state=0)

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
    initial_guess = deltas.median()
    guess = initial_guess
    data = align_data(data, guess / 2)

    change = max(0.1, guess / 10)
    no_probes = 101
    max_dim = len(data)
    data = np.expand_dims(data, 1)

    best = guess
    bestval = distance_metric(data % guess, guess)

    count = 0
    while change > 1e-4:
        probes = np.linspace(guess - guess * change, guess + guess * change, no_probes)
        results = np.mod(np.broadcast_to(data, (max_dim, no_probes)), probes)

        distances = distance_metric(results, probes)

        seed = np.argmin(distances)
        if distances[seed] < bestval:
            best = probes[seed]
            bestval = distances[seed]

        if seed < no_probes // 2:
            guess = guess - guess * change / 2
        elif seed > no_probes // 2:
            guess = guess + guess * change / 2
        change = change * 0.85
        count = count + 1
    best = best * round(initial_guess / best, 0)

    probes = np.linspace(best - 0.0002, best + 0.0002, no_probes)
    results = np.mod(np.broadcast_to(data, (max_dim, no_probes)), probes)

    distances = distance_metric(results, probes)

    seed = np.argmin(distances)
    if distances[seed] < bestval:
        best = probes[seed]

    return best


def align_data(data, new_offset):
    return data - data[0] + new_offset


def getOC(eclipses, return_diagnostics=False):
    """Using estimated period and offset, get the O-C values

    Args:
        eclipses: Pandas DataFrame containing eclipse timings, duration, and delta (time till previous eclipse)
        author: The person who coded out the period searching function

    Returns:
        O-C: An array of floats, representing the O-C values
    """

    filtered, diagnostics = complete_filter(eclipses, "delta", return_diagnositics=True)

    period = period_stupid_search(filtered['time'], filtered['delta'])

    period = period * round(filtered["delta"].median() / period, 0)
    filtered["residuals"] = align_data(filtered["time"], period / 2) % period - period / 2
    filtered = cull_oscillations(filtered, "residuals")

    # return  align_data(eclipses['time'], period / 2) % period, period

    if return_diagnostics:
        return filtered, period, diagnostics

    return filtered, period
