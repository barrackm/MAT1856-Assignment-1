import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_selected_bonds(csv_path, isins, dates):
    # Convert reference date to datetime object

    # Crease dictionary of selected bonds
    selected_bonds = dict()

    # Open file and read data
    with open(csv_path, 'r') as bond_file:
        # Open CSV using csv.DictReader
        reader = csv.DictReader(bond_file)

        # Iterate over rows in csv
        for row in reader:
            isin = row['ISIN']

            # Check if bond is selected bond using ISIN
            if isin not in isins:
                continue


            # Create new dict for single bond
            bond_data = dict()
            bond_data['ISIN'] = isin

            # Populate bond dict
            bond_data['coupon'] = float(row['coupon'])
            bond_data['maturity_date'] = row['maturity_date']

            # Convert prices to floats
            for date in dates:
                bond_data[date] = float(row[date])

            # Add bond to dictionary of selected bonds
            if isin not in selected_bonds:
                selected_bonds[isin] = bond_data

    return selected_bonds


def get_years_to_maturity(ref_date, bond):
    maturity_datetime = datetime.strptime(bond['maturity_date'], '%Y-%m-%d').date()
    ref_datetime =  datetime.strptime(ref_date, '%Y-%m-%d').date()

    return (maturity_datetime - ref_datetime).days / 365

def get_days_since_coupon(ref_date, bond):
    maturity_datetime = datetime.strptime(bond['maturity_date'], '%Y-%m-%d').date()
    ref_datetime = datetime.strptime(ref_date, '%Y-%m-%d').date()

    last_coupon_date = maturity_datetime
    while ref_datetime < last_coupon_date:
        last_coupon_date = last_coupon_date + relativedelta(months=-6)
    days_since_coupon = (ref_datetime - last_coupon_date).days

    return days_since_coupon
