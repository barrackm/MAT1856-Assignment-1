import numpy as np
from Helper import *

def get_forward_rates(spot_times, spot_rates, price_dates, resolution=10):
    # This function is designed to return the forward rate curves with terms ranging from 2-5 years

    # Define arrays to store forward rates and times for plotting
    all_times = dict()
    all_rates = dict()

    for date in price_dates:
        times = spot_times[date]
        rates = spot_rates[date]

        # Forward rates and times from 1-1 through 1-4
        T = [3 * i / (resolution - 1) + 2 for i in range(resolution)]
        f = np.zeros(resolution)

        # Use builtin numpy function to interpolate S_1 from the spot rates
        S_1 = np.interp(1, times, rates)

        # Calculate S_1T using interpolation
        for i in range(resolution):
            S_1T = np.interp(T[i], times, rates)

            # Calculate forward rate
            f[i] = (S_1T * T[i] - S_1) / (T[i] - 1)

        all_times[date] =  T
        all_rates[date] = f

    return all_times, all_rates
