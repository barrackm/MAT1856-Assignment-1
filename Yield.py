from Helper import *
import numpy as np
from scipy.optimize import brentq



def get_price_from_yield(y, coupon_payment, notional, remaining_coupons, t):
    present_value = 0
    for j in range(remaining_coupons):
        present_value += coupon_payment * np.exp(-1 * y * j / 2)

    present_value += notional * np.exp(-1 * y * t)
    return present_value


def get_ytm(selected_bonds, price_dates):
    # Define arrays to store yields and times for plotting
    all_times = dict()
    all_yields = dict()

    for date in price_dates:
        yields = np.zeros(len(selected_bonds.values()))
        times = np.zeros_like(yields)

        # Loop over bonds to construct yield curve
        for i, bond in enumerate(sorted(selected_bonds.values(), key=lambda x: x['maturity_date'])):
            # Get semi-annual coupon payment amount
            coupon_payment = bond['coupon'] / 2

            # Get notional value
            notional = 100 + coupon_payment

            # Get number of days since last coupon
            n = get_days_since_coupon(date, bond)

            # Calculated accrued interest
            accrued_interest = coupon_payment * n / 180

            # Use accrued interest to calculate the dirty price
            dirty_price = bond[date] + accrued_interest

            # Get years to maturity
            t = get_years_to_maturity(date, bond)

            # Save in times array for plotting curve
            times[i] = t

            # Get remaining number of coupon payments prior to maturity3
            remaining_coupons = int(t // 0.5)

            # Directly compute yield if no coupons remaining
            if remaining_coupons == 0:
                yields[i] = -1 * np.log(dirty_price / notional) / t

            # Compute next rate in chain
            else:
                def objective(y):
                    return get_price_from_yield(y, coupon_payment, notional, remaining_coupons, t) - dirty_price

                try:
                    sol = brentq(objective, a=-0.01, b=0.30)
                    yields[i] = sol
                except:
                    print("No solution found")
                    yields[i] = -1

        all_times[date] = times
        all_yields[date] = yields
    return all_times, all_yields

