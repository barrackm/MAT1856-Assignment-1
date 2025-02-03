import numpy as np


def get_RV_matrix(times, rates, price_dates, maturities):
    # Create matrix with proper shape
    RV_matrix = np.zeros((len(maturities), len(price_dates) - 1))

    # Populate matric with log-rates
    for i, m in enumerate(maturities):
        for j, date in enumerate(price_dates[:-1]):
            times_j = times[date]
            times_jp1 = times[price_dates[j + 1]]

            rates_j = rates[date]
            rates_jp1 = rates[price_dates[j + 1]]

            r_ij = np.interp(m, times_j, rates_j)
            r_ijp1 = np.interp(m, times_jp1, rates_jp1)

            RV_matrix[i, j] = np.log(r_ijp1 / r_ij)
    return RV_matrix

def get_covariance_matrix(times, rates, price_dates, maturities):
    # Create matrix of RVs and return covariance matrix
    RV_matrix = get_RV_matrix(times, rates, price_dates, maturities)
    return np.cov(RV_matrix)