from Helper import *
import numpy as np

def get_spot_rates(selected_bonds, price_dates):
    # Define arrays to store rates and times for plotting
    all_times = dict()
    all_rates = dict()

    for date in price_dates:
        # Define arrays to store yields and times for plotting
        rates = np.zeros(len(selected_bonds.values()))
        times = np.zeros_like(rates)

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

            # Get remaining number of coupon payments prior to maturity
            remaining_coupons = int(t // 0.5)

            # Directly compute yield if no coupons remaining
            if remaining_coupons == 0:
                rates[i] = -1 * np.log(dirty_price / notional) / t

            # Compute next rate in chain
            else:
                payments = 0
                for j in range(remaining_coupons):
                    payments += coupon_payment * np.exp(-1 * rates[j] * times[j])

                rates[i] = -np.log((dirty_price - payments) / notional) / t

        all_times[date] = times
        all_rates[date] = rates
    return all_times, all_rates
