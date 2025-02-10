import pandas as pd

def load_data(file_path):
    """
    Load the Excel file and return the data as a DataFrame.

    :param file_path: Path to the Excel file containing the data.
    :return: A pandas DataFrame with the loaded data.
    """
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None

def get_unique_subheaders(data, cif):
    """
    Retrieve unique SUBHEADER values based on the given CIF and specific TRX_TYPE conditions.

    :param data: The pandas DataFrame containing the data.
    :param cif: The CIF value to filter the data.
    :return: A list of unique SUBHEADER values that match the criteria.
    """
    try:
        # Filter the data based on CIF and TRX_TYPE conditions
        filtered_data = data[
            (data['CIF'] == cif) &
            ((data['TRX_TYPE'] == 'Pembayaran') | (data['TRX_TYPE'] == 'Pembayaran Qris'))
        ]

        # Return unique SUBHEADER values
        return filtered_data['SUBHEADER'].unique().tolist()
    except Exception as e:
        print(f"An error occurred during data filtering: {e}")
        return []
