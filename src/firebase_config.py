import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage
from dotenv import load_dotenv
import streamlit as st

# Load environment variables (for local development)
load_dotenv()


def initialize_firebase():
    """Initialize Firebase Admin SDK with credentials and return app instance."""
    try:
        # Check if app is already initialized to prevent multiple initializations
        firebase_admin.get_app()
        return firebase_admin.get_app()
    except ValueError:
        # App not initialized yet, continue with initialization
        pass

    try:
        # First, try Streamlit secrets (for Streamlit Cloud)
        if hasattr(st, 'secrets') and 'textkey' in st.secrets:
            # Parse the JSON string from secrets
            service_account_info = json.loads(st.secrets['textkey'])
            cred = credentials.Certificate(service_account_info)

            # Get storage bucket from secrets or None if not available
            storage_bucket = st.secrets.get('FIREBASE_STORAGE_BUCKET', None)
        else:
            # Fallback to local file (for local development)
            if os.path.exists('firebase-key.json'):
                cred = credentials.Certificate('firebase-key.json')
            else:
                raise FileNotFoundError("Firebase credentials file not found")

            # Get from environment variable
            storage_bucket = os.getenv('FIREBASE_STORAGE_BUCKET')

        # Initialize Firebase app
        if storage_bucket:
            firebase_admin.initialize_app(cred, {
                'storageBucket': storage_bucket
            })
        else:
            # Initialize without storage if bucket not specified
            firebase_admin.initialize_app(cred)

        return firebase_admin.get_app()
    except Exception as e:
        # Re-raise with additional context
        raise Exception(f"Firebase initialization failed: {str(e)}")


def get_firestore_db():
    """Get Firestore database client."""
    app = initialize_firebase()
    return firestore.client(app)


def get_storage_bucket():
    """Get Firebase Storage bucket."""
    app = initialize_firebase()
    try:
        return storage.bucket(app=app)
    except Exception as e:
        print(f"Warning: Storage bucket not available - {str(e)}")
        return None
