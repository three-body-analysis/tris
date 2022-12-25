import numpy as np
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
    regressor.fit(x_train, y_train) #training the algorithm

    # Print the error of estimation
    print("MSE of estimation", metrics.mean_squared_error(y_test, regressor.predict(x_test)))
    return regressor.coef_[0], regressor.intercept_


def getOC(timings, period = -1, offset = -1):
    """Using estimated period and offset, get the O-C values

    Args:
        timings (1D Array of floats): A list of eclipse TOMs
        period (int, optional): For precalculated values, leave blank to calculate.
        offset (int, optional): For precalculated values, leave blank to calculate.

    Returns:
        O-C: An array of floats, representing the O-C values
    """


    if (period == -1 and offset == -1):
        period, offset = estimateConstantPeriod(timings)

    if (period == -1): period = 0
    if (offset == -1): offset = 0

    return timings - offset - np.arange(len(timings)) * period