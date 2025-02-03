from Helper import *
from Yield import *
from Spot import *
from Forward import *
from Coviariance import *
from matplotlib import pyplot as plt

# Path to bond data
bond_path = 'bond_data.csv'

# Selected bond ISINs
selected_isins = ['CA135087K528', 'CA135087K940', 'CA135087L518',
                  'CA135087L930', 'CA135087M847', 'CA135087N837',
                  'CA135087P576', 'CA135087Q491', 'CA135087Q988',
                  'CA135087R895', 'CA135087S471']


# Days with price data
price_dates = ['2025-01-06', '2025-01-07', '2025-01-08',
               '2025-01-09', '2025-01-10', '2025-01-13',
               '2025-01-14', '2025-01-15', '2025-01-16',
               '2025-01-17']

# Load in data for selected bonds
selected_bonds = load_selected_bonds(bond_path, selected_isins, price_dates)

# Get YTM
ytm_t, ytm_r = get_ytm(selected_bonds, price_dates)

# Get Spot rates
spot_t, spot_r = get_spot_rates(selected_bonds, price_dates)

# Get forward rates
forward_t, forward_r = get_forward_rates(spot_t, spot_r, price_dates)

# Define maturity times for log-returns of yield
maturities = [i + 1 for i in range(5)]

# Get ytm covariance matrix
ytm_cov = get_covariance_matrix(ytm_t, ytm_r, price_dates, maturities)



# Get eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(ytm_cov)

# Use argsort to sort eigenvectors by eigenvalue
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

print(f"For daily log-returns of yield, Covariance Matrix:\n {ytm_cov} \nEigenvalues:\n {eigenvalues} \nEigenvectors:\n {np.round(eigenvectors, 4)}")

# Define maturity times for log-returns of yield
maturities = [i + 2 for i in range(4)]

# Get ytm covariance matrix
forward_cov = get_covariance_matrix(forward_t, forward_r, price_dates, maturities)

# Get eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(forward_cov)

# Use argsort to sort eigenvectors by eigenvalue
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

print(f"For daily log-forward rates, Covariance Matrix:\n {forward_cov} \nEigenvalues:\n {eigenvalues} \nEigenvectors:\n {np.round(eigenvectors, 4)}")


# Plot YTM curves
plt.figure(figsize=(12, 5))

for date in price_dates:
    plt.plot(ytm_t[date], ytm_r[date]*100, label=date)

plt.title("5-Year Yield Curve (ytm curve)")
plt.ylabel("Yield (%)")
plt.xlabel("Time to Maturity (years)")
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()


# Plot Spot curves
plt.figure(figsize=(12, 5))

for date in price_dates:
    times = spot_t[date]
    indices = times > 1
    times = times[indices]
    rates = spot_r[date][indices]
    plt.plot(times, rates*100, label=date)

plt.title("1-5 Year Spot Curve")
plt.ylabel("Spot Rate (%)")
plt.xlabel("Time to Maturity (years)")
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

# Plot Forwards curves
plt.figure(figsize=(12, 5))

for date in price_dates:
    plt.plot(forward_t[date], forward_r[date]*100, label=date)

plt.title("2-5 Year Forward Curve")
plt.ylabel("Yield (%)")
plt.xlabel("Time (years)")
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

