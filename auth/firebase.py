import os
import pyrebase
import firebase_admin

from dotenv import load_dotenv

from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()

# ----------------------------
# Firebase Web Configuration
# ----------------------------

firebase_config = {

    "apiKey": os.getenv("FIREBASE_API_KEY"),

    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),

    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),

    "projectId": os.getenv("FIREBASE_PROJECT_ID"),

    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),

    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),

    "appId": os.getenv("FIREBASE_APP_ID")

}

# ----------------------------
# Pyrebase Authentication
# ----------------------------

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

# ----------------------------
# Firebase Admin SDK
# ----------------------------

if not firebase_admin._apps:

    cred = credentials.Certificate(
        os.getenv("FIREBASE_SERVICE_ACCOUNT")
    )

    firebase_admin.initialize_app(cred)

# ----------------------------
# Firestore Database
# ----------------------------

db = firestore.client()