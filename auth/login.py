from auth.firebase import auth, db
from datetime import datetime


def login(email, password):
    """
    Login using Firebase Authentication.
    Load the user's Firestore profile.
    """

    try:

        # -----------------------------
        # Firebase Authentication
        # -----------------------------
        user = auth.sign_in_with_email_and_password(
            email,
            password
        )

        user_id = user["localId"]

        # -----------------------------
        # Firestore User Document
        # -----------------------------
        user_ref = db.collection("users").document(user_id)

        document = user_ref.get()

        # If somehow the document doesn't exist,
        # create a default profile.
        if not document.exists:

            user_ref.set({

                "uid": user_id,

                "email": user["email"],

                "display_name": "",

                "username": "",

                "profile_completed": False,

                "provider": "email",

                "created_at": datetime.utcnow(),

                "last_login": datetime.utcnow()

            })

            profile = user_ref.get().to_dict()

        else:

            profile = document.to_dict()

            user_ref.update({

                "last_login": datetime.utcnow()

            })

        # -----------------------------
        # Merge Authentication Data
        # -----------------------------
        user["profile"] = profile

        return True, user

    except Exception as e:

        return False, str(e)