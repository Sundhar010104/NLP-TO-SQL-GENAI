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

    # 1. Check Streamlit secrets dictionary or nested section
    try:
        if hasattr(st, "secrets"):
            for sec_key in ["firebase_service_account", "FIREBASE_SERVICE_ACCOUNT", "gcp_service_account", "service_account"]:
                if sec_key in st.secrets:
                    sec_val = st.secrets[sec_key]
                    if isinstance(sec_val, str):
                        try:
                            cred_data = json.loads(sec_val)
                        except Exception:
                            cred_data = sec_val
                    else:
                        cred_data = dict(sec_val)
                    break

            # 1b. Check if service account fields are defined flat at root of st.secrets
            if cred_data is None and "private_key" in st.secrets and "client_email" in st.secrets:
                cred_data = {
                    "type": st.secrets.get("type", "service_account"),
                    "project_id": st.secrets.get("project_id", get_config_val("FIREBASE_PROJECT_ID")),
                    "private_key_id": st.secrets.get("private_key_id", ""),
                    "private_key": st.secrets.get("private_key"),
                    "client_email": st.secrets.get("client_email"),
                    "client_id": st.secrets.get("client_id", ""),
                    "auth_uri": st.secrets.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
                    "token_uri": st.secrets.get("token_uri", "https://oauth2.googleapis.com/token"),
                    "auth_provider_x509_cert_url": st.secrets.get("auth_provider_x509_cert_url", "https://www.googleapis.com/oauth2/v1/certs"),
                    "client_x509_cert_url": st.secrets.get("client_x509_cert_url", ""),
                    "universe_domain": st.secrets.get("universe_domain", "googleapis.com")
                }
    except Exception:
        pass

    # 2. Check environment variables
    if cred_data is None:
        for env_key in ["FIREBASE_SERVICE_ACCOUNT", "FIREBASE_SERVICE_ACCOUNT_JSON", "GCP_SERVICE_ACCOUNT"]:
            env_val = os.getenv(env_key)
            if env_val:
                if isinstance(env_val, str) and os.path.exists(env_val):
                    cred_data = env_val
                    break
                else:
                    try:
                        cred_data = json.loads(env_val)
                        break
                    except Exception:
                        pass

    # 3. Fallback for local development: check for local service account JSON file
    if cred_data is None:
        json_files = glob.glob("*-firebase-adminsdk-*.json")
        if json_files:
            cred_data = json_files[0]

    # Initialize Firebase Admin credential
    if cred_data:
        try:
            if isinstance(cred_data, str):
                if os.path.exists(cred_data):
                    cred = credentials.Certificate(cred_data)
                else:
                    parsed = json.loads(cred_data)
                    if "private_key" in parsed and isinstance(parsed["private_key"], str):
                        parsed["private_key"] = parsed["private_key"].replace("\\n", "\n")
                    cred = credentials.Certificate(parsed)
            elif isinstance(cred_data, dict):
                cred_copy = dict(cred_data)
                if "private_key" in cred_copy and isinstance(cred_copy["private_key"], str):
                    cred_copy["private_key"] = cred_copy["private_key"].replace("\\n", "\n")
                cred = credentials.Certificate(cred_copy)
            else:
                cred = credentials.Certificate(cred_data)

            firebase_admin.initialize_app(cred)
        except Exception as err:
            st.error(f"⚠️ **Firebase Credential Error:** Failed to initialize Firebase Admin SDK. Details: {err}")
            st.stop()
    else:
        st.error(
            "⚠️ **Firebase Service Account Credentials Missing!**\n\n"
            "If you are deploying on Streamlit Cloud, please add your Firebase credentials under **App Settings > Secrets**.\n\n"
            "Refer to the instructions to add `[firebase_service_account]` in your Streamlit secrets."
        )
        st.stop()

# ----------------------------
# Firestore Database
# ----------------------------

db = firestore.client()

