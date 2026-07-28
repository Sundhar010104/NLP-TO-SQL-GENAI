import streamlit as st
import pandas as pd

# -----------------------------
# Authentication Imports
# -----------------------------
from auth.login import login
from auth.signup import signup
from auth.firebase import db

# -----------------------------
# NLP-SQL Imports
# -----------------------------
from utils.uploader import load_dataset
from database.db import save_to_database, list_tables
from database.schema import get_schema
from llm.prompts import SQL_PROMPT
from llm.gemini import ask_gemini
from sql.validator import validate_sql
from sql.executor import execute_query

from database.history import (
    save_current_chat,
    show_chat_history,
    display_chat,
)
# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="NLP to SQL Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Session Initialization
# -----------------------------
from auth.session import (
    initialize_session,
    login_user,
    logout_user,
    is_logged_in,
    current_user
)

initialize_session()

# =============================
# AUTHENTICATION SCREEN
# =============================
if not is_logged_in():

    st.title("🤖 NLP to SQL Chatbot")

    st.markdown("## Login / Sign Up")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ---------------- Login ----------------
    with tab1:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            success, user = login(email, password)

            if success:

                login_user(user)

                st.success("Login Successful")

                st.rerun()

            else:

                st.error(user)

    # ---------------- Signup ----------------
    with tab2:

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        if st.button("Create Account", use_container_width=True):

            success, message = signup(email, password)

            if success:

                st.success(
                    "Account created successfully.\nPlease login."
                )

            else:

                st.error(message)

    st.stop()
# ==========================================
# COMPLETE PROFILE (FIRST LOGIN ONLY)
# ==========================================

if not st.session_state.profile_completed:

    st.title("👋 Welcome!")

    st.markdown("### Complete your profile")

    display_name = st.text_input(
        "Display Name",
        placeholder="Ex: Sundharesan KP"
    )

    username = st.text_input(
        "Username",
        placeholder="Ex: sundhar"
    )

    if st.button("Save Profile", use_container_width=True):

        if display_name.strip() == "" or username.strip() == "":

            st.warning("Please fill all fields.")

        else:

            db.collection("users").document(
                st.session_state.user_id
            ).update({

                "display_name": display_name,

                "username": username,

                "profile_completed": True

            })

            st.session_state.display_name = display_name

            st.session_state.username = username

            st.session_state.profile_completed = True

            st.success("Profile saved successfully!")

            st.rerun()

# =============================
# SIDEBAR
# =============================
user = current_user()

st.sidebar.markdown("# 👋 Welcome")

st.sidebar.markdown(
    f"### {user['display_name']}"
)

st.sidebar.caption(
    f"@{user['username']}"
)

st.sidebar.write(user["email"])

st.sidebar.divider()

if st.sidebar.button("Logout"):

    logout_user()
selected_chat = show_chat_history(
    st.session_state.user_id
)

if selected_chat:
    display_chat(selected_chat)

# =============================
# MAIN APPLICATION
# =============================

st.title("🤖 NLP to SQL Chatbot")
st.write("Upload a CSV or Excel file and ask questions in natural language.")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    df = load_dataset(uploaded_file)

    # OPTIONAL
    # Make table unique for each user
    user_id = st.session_state.user["localId"]

    table_name = f"{user_id}_{uploaded_file.name.split('.')[0]}"

    save_to_database(df, table_name)

    st.success("✅ Dataset uploaded successfully.")

    st.subheader("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )

    tables = list_tables()

    st.subheader("📋 Available Tables")

    table_df = pd.DataFrame(
        tables,
        columns=["Table Name"]
    )

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.header("💬 Ask Questions")

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Generate SQL"):

        if question.strip() == "":

            st.warning("Please enter a question.")

            st.stop()

        schema = get_schema()

        prompt = SQL_PROMPT.format(
            schema=schema,
            question=question
        )

        sql = ask_gemini(prompt)

        st.subheader("Generated SQL")

        st.code(sql, language="sql")

        valid, message = validate_sql(sql)

        if not valid:

            st.error(message)

            st.stop()

        status, result = execute_query(sql)

        if status:

            st.success("✅ Query Executed Successfully")

            st.subheader("Query Results")

            st.dataframe(
                result,
                width = "stretch"
            )
            save_current_chat(
               user_id=st.session_state.user_id,
               question=question,
               sql=sql,
               result=result
            )

        else:

            st.error(result)

else:

    st.info("📁 Please upload a CSV or Excel file.")