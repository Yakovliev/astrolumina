# import pandas as pd

# # Map numeric Star type to category names if needed
# star_type_mapping = {
#     0: 'Brown Dwarf',
#     1: 'Red Dwarf',
#     2: 'White Dwarf',
#     3: 'Main Sequence',
#     4: 'Supergiants',
#     5: 'Hypergiants'
# }


# def load_star_data(file_path='data/cleaned_star_data.csv'):
#     """
#     Load star data from CSV file and perform initial processing.

#     Parameters:
#     file_path (str): Path to the CSV file

#     Returns:
#     pandas.DataFrame: Processed DataFrame
#     """
#     # Load the data
#     df = pd.read_csv(file_path)

#     # Check if Star type is numeric and needs mapping
#     if pd.api.types.is_numeric_dtype(df['Star type']):
#         df['Star type'] = df['Star type'].map(star_type_mapping)

#     return df

import pandas as pd
import os
import streamlit as st

# Map numeric Star type to category names if needed
star_type_mapping = {
    0: 'Brown Dwarf',
    1: 'Red Dwarf',
    2: 'White Dwarf',
    3: 'Main Sequence',
    4: 'Supergiants',
    5: 'Hypergiants'
}


def load_star_data(use_firestore=True, file_path='data/cleaned_star_data.csv'):
    """
    Load star data from Firestore or CSV file and perform initial processing.

    Parameters:
    use_firestore (bool): Whether to use Firestore as the data source
    file_path (str): Path to the CSV file (used as fallback)

    Returns:
    pandas.DataFrame: Processed DataFrame
    """
    if use_firestore:
        try:
            # Try to import Firebase modules
            try:
                from src.firebase_config import get_firestore_db
            except ImportError:
                st.warning(
                    "Firebase modules not available. Falling back to CSV.")
                return load_star_data(use_firestore=False, file_path=file_path)

            # Get Firestore database client
            db = get_firestore_db()

            # Reference to stars collection
            stars_ref = db.collection('stars')

            # Get all documents from the collection
            stars_docs = stars_ref.stream()

            # Convert Firestore documents to a list of dictionaries
            stars_data = [doc.to_dict() for doc in stars_docs]

            # Create DataFrame from list of dictionaries
            df = pd.DataFrame(stars_data)

            # Check if data was retrieved
            if df.empty:
                print("No data found in Firestore. Falling back to CSV.")
                return load_star_data(use_firestore=False, file_path=file_path)

            print(f"Successfully loaded {len(df)} records from Firestore.")

        except Exception as e:
            print(f"Error loading data from Firestore: {e}")
            print("Falling back to CSV file.")
            return load_star_data(use_firestore=False, file_path=file_path)
    else:
        # Load from CSV (fallback method)
        print(f"Loading data from CSV: {file_path}")
        df = pd.read_csv(file_path)

    # Check if Star type is numeric and needs mapping
    if 'Star type' in df.columns:
        if pd.api.types.is_numeric_dtype(df['Star type']):
            df['Star type'] = df['Star type'].map(star_type_mapping)
        # Ensure star type is string (this is crucial for Plotly visualizations)
        df['Star type'] = df['Star type'].astype(str)

    return df


def get_star_types():
    """
    Get list of unique star types from the data.

    Returns:
    list: List of unique star types
    """
    try:
        # Try to use Firestore
        try:
            from src.firebase_config import get_firestore_db
            db = get_firestore_db()
            stars_ref = db.collection('stars')
            docs = stars_ref.stream()
            star_types = set()

            for doc in docs:
                data = doc.to_dict()
                if 'Star type' in data:
                    star_types.add(data['Star type'])

            return sorted(list(star_types))
        except Exception:
            # Fallback to CSV if Firestore fails
            df = load_star_data(use_firestore=False)
            return sorted(df['Star type'].unique().tolist())

    except Exception as e:
        print(f"Error fetching star types: {e}")
        return []
