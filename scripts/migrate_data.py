# TO RUN FROM THE ROOT DIRECTORY

from src.firebase_config import get_firestore_db
import pandas as pd
import numpy as np
import sys
import os
import importlib.util

# Define star type mapping here to avoid circular imports
star_type_mapping = {
    0: 'Brown Dwarf',
    1: 'Red Dwarf',
    2: 'White Dwarf',
    3: 'Main Sequence',
    4: 'Supergiants',
    5: 'Hypergiants'
}


def migrate_csv_to_firestore(csv_path='data/cleaned_star_data.csv', batch_size=100):
    """
    Migrate star data from CSV to Firestore.

    Parameters:
    csv_path (str): Path to the CSV file
    batch_size (int): Number of documents to write in each batch
    """
    print(f"Starting migration from {csv_path} to Firestore...")

    # Load CSV data
    df = pd.read_csv(csv_path)

    # Initialize Firestore
    db = get_firestore_db()

    # Reference to stars collection
    stars_ref = db.collection('stars')

    # Count total documents before migration
    doc_count_before = len(list(stars_ref.limit(1000).stream()))
    print(f"Current document count in 'stars' collection: {doc_count_before}")

    # Create a batch for Firestore writes
    batch = db.batch()

    count = 0
    total = len(df)
    batch_count = 0

    for index, row in df.iterrows():
        # Convert row to dictionary
        star_data = row.to_dict()

        # If Star type is numeric, add the label
        if isinstance(star_data['Star type'], (int, np.integer)):
            star_data['Star type label'] = star_type_mapping.get(
                star_data['Star type'], f"Unknown Type {star_data['Star type']}")

        # Create a document reference with a generated ID
        doc_ref = stars_ref.document()

        # Add data to batch
        batch.set(doc_ref, star_data)

        count += 1
        batch_count += 1

        # Commit batch when it reaches the batch size
        if batch_count >= batch_size:
            batch.commit()
            print(f"Committed batch: {count}/{total} documents")
            batch = db.batch()
            batch_count = 0

    # Commit any remaining documents
    if batch_count > 0:
        batch.commit()
        print(f"Committed final batch: {count}/{total} documents")

    # Count total documents after migration
    doc_count_after = len(list(stars_ref.limit(1000).stream()))
    print(f"Document count after migration: {doc_count_after}")
    print(f"Added {doc_count_after - doc_count_before} documents")
    print("Migration completed!")


if __name__ == "__main__":
    migrate_csv_to_firestore()
