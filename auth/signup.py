from auth.firebase import auth, db
from datetime import datetime


def signup(email, password):
    """
    Create a Firebase Authentication account and
    initialize the user's Firestore profile.
    """

    try:

        # -----------------------------
        # Create Firebase Authentication User
        # -----------------------------
        user = auth.create_user_with_email_and_password(
            email,
            password
        )

        user_id = user["localId"]

        # -----------------------------
        # Create Firestore User Profile
        # -----------------------------
        db.collection("users").document(user_id).set({

            "uid": user_id,

            "email": email,

            # Profile fields (filled after first login)
            "display_name": "",

            "username": "",

            "profile_completed": False,

            # Authentication Provider
            "provider": "email",

            # Dates
            "created_at": datetime.utcnow(),

            "last_login": datetime.utcnow()

        })

        return True, user

    except Exception as e:

        return False, str(e)