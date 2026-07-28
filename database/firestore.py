from auth.firebase import db
from google.cloud.firestore import SERVER_TIMESTAMP


# ==========================================
# Users Collection
# ==========================================

def get_user_document(user_id):
    """
    Returns the Firestore document reference
    for a specific user.
    """
    return db.collection("users").document(user_id)


# ==========================================
# Chat Collection
# ==========================================

def get_chat_collection(user_id):
    """
    Returns the chat_history collection
    of a particular user.
    """
    return (
        db.collection("users")
        .document(user_id)
        .collection("chat_history")
    )


# ==========================================
# Save Chat
# ==========================================

from auth.firebase import db
from google.cloud.firestore import SERVER_TIMESTAMP


def save_chat(user_id, question, sql, result):
    try:
        chat = {
            "question": question,
            "sql": sql,
            "result": result,
            "timestamp": SERVER_TIMESTAMP
        }

        doc = (
            db.collection("users")
            .document(user_id)
            .collection("chat_history")
            .add(chat)
        )

        print("Firestore Save Success:", doc)

    except Exception as e:
        print("Firestore Error:", e)
        raise e

# ==========================================
# Load Chats
# ==========================================

def load_chats(user_id):
    """
    Returns all chats ordered by time.
    """

    docs = (
        get_chat_collection(user_id)
        .order_by("timestamp", direction="DESCENDING")
        .stream()
    )

    chats = []

    for doc in docs:

        data = doc.to_dict()

        data["id"] = doc.id

        chats.append(data)

    return chats


# ==========================================
# Delete Chat
# ==========================================

def delete_chat(user_id, chat_id):
    """
    Delete a single conversation.
    """

    (
        get_chat_collection(user_id)
        .document(chat_id)
        .delete()
    )


# ==========================================
# Delete All Chats
# ==========================================

def delete_all_chats(user_id):
    """
    Delete every chat belonging to a user.
    """

    docs = get_chat_collection(user_id).stream()

    for doc in docs:

        doc.reference.delete()


# ==========================================
# Update Chat
# ==========================================

def update_chat(user_id, chat_id, question, sql, result):
    """
    Update an existing conversation.
    """

    (
        get_chat_collection(user_id)
        .document(chat_id)
        .update({

            "question": question,

            "sql": sql,

            "result": result

        })
    )


# ==========================================
# Get One Chat
# ==========================================

def get_chat(user_id, chat_id):
    """
    Returns one specific conversation.
    """

    doc = (
        get_chat_collection(user_id)
        .document(chat_id)
        .get()
    )

    if doc.exists:

        return doc.to_dict()

    return None