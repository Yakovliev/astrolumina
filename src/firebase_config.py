import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def initialize_firebase():
    """Initialize Firebase Admin SDK with credentials and return app instance."""
    try:
        # Check if app is already initialized to prevent multiple initializations
        firebase_admin.get_app()
    except ValueError:
        # Load service account key
        cred = credentials.Certificate('firebase-key.json')

        # Initialize Firebase app
        firebase_admin.initialize_app(cred, {
            'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
        })

    return firebase_admin.get_app()


def get_firestore_db():
    """Get Firestore database client."""
    app = initialize_firebase()
    return firestore.client(app)


def get_storage_bucket():
    """Get Firebase Storage bucket."""
    app = initialize_firebase()
    return storage.bucket(app=app)
