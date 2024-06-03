import os
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
from pathlib import Path

# load env
load_dotenv()


def create_connection():
    try:
        # Load the credentials from the .env file from root directory
        cred = credentials.Certificate(Path(os.getcwd()).parent / os.getenv("FIREBASE_CREDENTIALS"))

        # Initialize the app with the credentials and the database URL
        firebase_app = initialize_app(cred, {
            'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
        })

        #test the connection
        print("Connection to Firebase successful")
        return firebase_app
    except Exception as e:
        print(f"Failed to connect to Firebase")
        print(f"Error: {e}")
        return None
