import streamlit as st
import pandas as pd

from database.firestore import (
    save_chat,
    load_chats,
    delete_chat,
    delete_all_chats,
)


# =====================================
# Save Current Conversation
# =====================================

def save_current_chat(user_id, question, sql, result):

    st.write("Saving chat...")
    st.write("User ID:", user_id)

    if isinstance(result, pd.DataFrame):
        result = result.to_dict(orient="records")

    save_chat(
        user_id=user_id,
        question=question,
        sql=sql,
        result=result
    )

    st.success("Chat saved successfully!")


# =====================================
# Sidebar Chat History
# =====================================

def show_chat_history(user_id):
    """
    Display chat history in the sidebar.
    """

    st.sidebar.markdown("## 💬 Chat History")

    chats = load_chats(user_id)

    if len(chats) == 0:
        st.sidebar.info("No chats yet.")
        return None

    selected_chat = None

    for chat in chats:

        question = chat.get("question", "Untitled")

        if len(question) > 35:
            question = question[:35] + "..."

        if st.sidebar.button(
            question,
            key=chat["id"],
            use_container_width=True
        ):
            selected_chat = chat

    st.sidebar.divider()

    if st.sidebar.button(
        "🗑 Clear All History",
        use_container_width=True
    ):
        delete_all_chats(user_id)
        st.rerun()

    return selected_chat


# =====================================
# Display Selected Chat
# =====================================

def display_chat(chat):

    if chat is None:
        return

    st.subheader("❓ Question")

    st.write(chat["question"])

    st.subheader("📝 SQL")

    st.code(
        chat["sql"],
        language="sql"
    )

    st.subheader("📊 Result")

    result = chat["result"]

    if isinstance(result, list):
        st.dataframe(pd.DataFrame(result))
    else:
        st.write(result)


# =====================================
# Delete One Chat
# =====================================

def remove_chat(user_id, chat_id):
    delete_chat(user_id, chat_id)