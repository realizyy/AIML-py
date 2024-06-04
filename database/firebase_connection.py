import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
from pathlib import Path

# load env
load_dotenv()

def create_connection():
    try:
        # Load the credentials from the .env file from root directory
        env_cred = Path(os.getcwd()) / os.getenv("FIREBASE_CREDENTIALS")
        cred = credentials.Certificate(Path(os.getcwd()) / os.getenv("FIREBASE_CREDENTIALS"))

        # Initialize the app with the credentials and the database URL
        env_url = os.getenv("FIREBASE_DATABASE_URL")
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
        })
        return db, env_url, env_cred
    except Exception as e:
        print(f'The error {e} occurred')
        return None
