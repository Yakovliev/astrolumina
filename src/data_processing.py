import pandas as pd

# Map numeric Star type to category names if needed
star_type_mapping = {
    0: 'Brown Dwarf',
    1: 'Red Dwarf',
    2: 'White Dwarf',
    3: 'Main Sequence',
    4: 'Supergiants',
    5: 'Hypergiants'
}


def load_star_data(file_path='data/cleaned_star_data.csv'):
    """
    Load star data from CSV file and perform initial processing.

    Parameters:
    file_path (str): Path to the CSV file

    Returns:
    pandas.DataFrame: Processed DataFrame
    """
    # Load the data
    df = pd.read_csv(file_path)

    # Check if Star type is numeric and needs mapping
    if pd.api.types.is_numeric_dtype(df['Star type']):
        df['Star type'] = df['Star type'].map(star_type_mapping)

    return df
