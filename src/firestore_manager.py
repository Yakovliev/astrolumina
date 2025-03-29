from src.firebase_config import get_firestore_db
import pandas as pd


class FirestoreManager:
    """Class to handle Firestore database operations for star data."""

    def __init__(self):
        """Initialize Firestore client."""
        self.db = get_firestore_db()
        self.stars_collection = 'stars'

    def get_all_stars(self):
        """
        Retrieve all stars from Firestore.

        Returns:
        pandas.DataFrame: DataFrame containing all star data
        """
        stars_ref = self.db.collection(self.stars_collection)
        docs = stars_ref.stream()

        stars_data = []
        for doc in docs:
            data = doc.to_dict()
            # Add document ID as a field
            data['id'] = doc.id
            stars_data.append(data)

        # Create DataFrame
        df = pd.DataFrame(stars_data) if stars_data else pd.DataFrame()

        # Convert 'Star type' to proper format
        if 'Star type' in df.columns:
            # Check if it's numeric and needs mapping
            if pd.api.types.is_numeric_dtype(df['Star type']):
                from src.data_processing import star_type_mapping
                df['Star type'] = df['Star type'].map(star_type_mapping)
            # Ensure star type is string for consistent display
            df['Star type'] = df['Star type'].astype(str)

        return df

    def get_stars_by_type(self, star_type):
        """
        Retrieve stars of a specific type.

        Parameters:
        star_type (str): Type of star to filter by

        Returns:
        pandas.DataFrame: DataFrame with filtered star data
        """
        stars_ref = self.db.collection(self.stars_collection)
        query = stars_ref.where('Star type', '==', star_type)
        docs = query.stream()

        stars_data = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            stars_data.append(data)

        return pd.DataFrame(stars_data) if stars_data else pd.DataFrame()

    def get_stars_by_color(self, star_color):
        """
        Retrieve stars of a specific color.

        Parameters:
        star_color (str): Color of star to filter by

        Returns:
        pandas.DataFrame: DataFrame with filtered star data
        """
        stars_ref = self.db.collection(self.stars_collection)
        query = stars_ref.where('Star color', '==', star_color)
        docs = query.stream()

        stars_data = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            stars_data.append(data)

        return pd.DataFrame(stars_data) if stars_data else pd.DataFrame()

    def get_unique_values(self, field):
        """
        Get unique values for a specific field.

        Parameters:
        field (str): Field name to get unique values for

        Returns:
        list: List of unique values
        """
        stars_ref = self.db.collection(self.stars_collection)
        docs = stars_ref.stream()

        values = set()
        for doc in docs:
            data = doc.to_dict()
            if field in data:
                values.add(data[field])

        return sorted(list(values))

    def add_star(self, star_data):
        """
        Add a new star to the database.

        Parameters:
        star_data (dict): Star data to add

        Returns:
        str: Document ID of the new star
        """
        doc_ref = self.db.collection(self.stars_collection).document()
        doc_ref.set(star_data)
        return doc_ref.id

    def update_star(self, star_id, star_data):
        """
        Update an existing star.

        Parameters:
        star_id (str): Document ID of the star to update
        star_data (dict): Updated star data

        Returns:
        bool: True if update was successful
        """
        doc_ref = self.db.collection(self.stars_collection).document(star_id)
        doc_ref.update(star_data)
        return True

    def delete_star(self, star_id):
        """
        Delete a star from the database.

        Parameters:
        star_id (str): Document ID of the star to delete

        Returns:
        bool: True if deletion was successful
        """
        doc_ref = self.db.collection(self.stars_collection).document(star_id)
        doc_ref.delete()
        return True

    def get_stars_in_range(self, field, min_value, max_value):
        """
        Get stars with a field value in a specific range.

        Parameters:
        field (str): Field to filter on
        min_value: Minimum value for the range
        max_value: Maximum value for the range

        Returns:
        pandas.DataFrame: DataFrame with filtered star data
        """
        stars_ref = self.db.collection(self.stars_collection)
        query = stars_ref.where(field, '>=', min_value).where(
            field, '<=', max_value)
        docs = query.stream()

        stars_data = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            stars_data.append(data)

        return pd.DataFrame(stars_data) if stars_data else pd.DataFrame()
