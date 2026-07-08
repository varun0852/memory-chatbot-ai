from datetime import datetime

from utils.chat_utils import generate_session_id


def reset_chat_session() -> None:
    """
    Reset the current chat session.

    This clears the conversation, removes the current
    chatbot instance, and generates a new session ID.
    """

    import streamlit as st

    st.session_state.messages = []

    if "chatbot" in st.session_state:
        del st.session_state.chatbot

    # Generate a conversation id
    st.session_state.session_id = generate_session_id()

    st.session_state.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
