import streamlit as st


# --------------------------------------
# Initialize Session Variables
# --------------------------------------
def initialize_session():

    defaults = {

        "logged_in": False,

        "user": None,

        "user_id": None,

        "email": None,

        "provider": None,

        # New Profile Fields
        "display_name": None,

        "username": None,

        "profile_completed": False

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# --------------------------------------
# Login User
# --------------------------------------
def login_user(user):

    profile = user.get("profile", {})

    st.session_state.logged_in = True

    st.session_state.user = user

    st.session_state.user_id = user["localId"]

    st.session_state.email = user["email"]

    st.session_state.provider = profile.get(
        "provider",
        "email"
    )

    # New Profile Information
    st.session_state.display_name = profile.get(
        "display_name",
        ""
    )

    st.session_state.username = profile.get(
        "username",
        ""
    )

    st.session_state.profile_completed = profile.get(
        "profile_completed",
        False
    )


# --------------------------------------
# Logout User
# --------------------------------------
def logout_user():

    keys = [

        "logged_in",

        "user",

        "user_id",

        "email",

        "provider",

        "display_name",

        "username",

        "profile_completed"

    ]

    for key in keys:

        st.session_state[key] = None

    st.session_state.logged_in = False

    st.session_state.profile_completed = False

    st.rerun()


# --------------------------------------
# Check Login Status
# --------------------------------------
def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )


# --------------------------------------
# Current User
# --------------------------------------
def current_user():

    return {

        "uid": st.session_state.get("user_id"),

        "email": st.session_state.get("email"),

        "provider": st.session_state.get("provider"),

        "display_name": st.session_state.get("display_name"),

        "username": st.session_state.get("username"),

        "profile_completed": st.session_state.get(
            "profile_completed"
        )

    }