import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_config_val(key, default=None):
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


GOOGLE_API_KEY = get_config_val("GOOGLE_API_KEY")

DATABASE_PATH = "data/database/chatbot.db"