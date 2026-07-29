import glob
import json
import os
import firebase_admin
import pyrebase
import streamlit as st
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

load_dotenv()


def get_config_val(key, default=None):
    """Retrieve configuration from Streamlit secrets if available, otherwise from environment variables."""
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


# ----------------------------
# Firebase Web Configuration
# ----------------------------

firebase_config = {
    "apiKey": get_config_val("FIREBASE_API_KEY"),
    "authDomain": get_config_val("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": get_config_val("FIREBASE_DATABASE_URL"),
    "projectId": get_config_val("FIREBASE_PROJECT_ID"),
    "storageBucket": get_config_val("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": get_config_val("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": get_config_val("FIREBASE_APP_ID"),
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
    cred_data = None

    # 1. Check Streamlit secrets dictionary or string
    try:
        if hasattr(st, "secrets"):
            if "firebase_service_account" in st.secrets:
                sec_val = st.secrets["firebase_service_account"]
                cred_data = dict(sec_val) if not isinstance(sec_val, str) else sec_val
            elif "FIREBASE_SERVICE_ACCOUNT" in st.secrets:
                sec_val = st.secrets["FIREBASE_SERVICE_ACCOUNT"]
                cred_data = dict(sec_val) if not isinstance(sec_val, str) else sec_val
    except Exception:
        pass

    # 2. Check environment variable
    if cred_data is None:
        env_val = os.getenv("FIREBASE_SERVICE_ACCOUNT")
        if env_val:
            if isinstance(env_val, str) and os.path.exists(env_val):
                cred_data = env_val
            else:
                try:
                    cred_data = json.loads(env_val)
                except Exception:
                    pass

    # 3. Fallback for local development: check for local service account JSON file
    if cred_data is None:
        json_files = glob.glob("*-firebase-adminsdk-*.json")
        if json_files:
            cred_data = json_files[0]

    # Initialize Firebase Admin credential
    if cred_data:
        if isinstance(cred_data, str):
            if os.path.exists(cred_data):
                cred = credentials.Certificate(cred_data)
            else:
                # Try parsing as JSON string
                parsed = json.loads(cred_data)
                if "private_key" in parsed and isinstance(parsed["private_key"], str):
                    parsed["private_key"] = parsed["private_key"].replace("\\n", "\n")
                cred = credentials.Certificate(parsed)
        elif isinstance(cred_data, dict):
            if "private_key" in cred_data and isinstance(cred_data["private_key"], str):
                cred_data["private_key"] = cred_data["private_key"].replace("\\n", "\n")
            cred = credentials.Certificate(cred_data)
        else:
            cred = credentials.Certificate(cred_data)

        firebase_admin.initialize_app(cred)
    else:
        raise ValueError(
            "Firebase Service Account credentials not found. Please provide FIREBASE_SERVICE_ACCOUNT "
            "in Streamlit secrets, environment variables, or a local service account JSON file."
        )

# ----------------------------
# Firestore Database
# ----------------------------

db = firestore.client()
