import toml
import os
import json
from dotenv import load_dotenv

# Load environment variables to get storage bucket
load_dotenv()

output_file = ".streamlit/secrets.toml"

# Make sure the .streamlit directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Read the Firebase key as a JSON object
with open("firebase-key.json") as json_file:
    firebase_key = json.load(json_file)

# Convert JSON to a properly formatted string
firebase_json_string = json.dumps(firebase_key)

# Create the config with both Firebase key and storage bucket
config = {
    "textkey": firebase_json_string,
    "FIREBASE_STORAGE_BUCKET": os.getenv("FIREBASE_STORAGE_BUCKET", "")
}

# Convert to TOML and write to file
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)

print(f"Created {output_file} with Firebase key and storage bucket")
