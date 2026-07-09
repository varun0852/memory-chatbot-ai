"""
Session initialization utilities.
"""

from datetime import datetime

import streamlit as st

from config import DEFAULT_MODEL

from utils.chat_utils import generate_session_id


def initialize_session_state() -> None:
    """
    Initialize the Streamlit session state.

    Creates all required session state variables with
    their default values if they do not already exist.
    Existing values are preserved.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "document_text" not in st.session_state:
        st.session_state.document_text = None

    if "document_name" not in st.session_state:
        st.session_state.document_name = None

    if "import_key" not in st.session_state:
        st.session_state.import_key = 0

    if "show_import_success" not in st.session_state:
        st.session_state.show_import_success = False

    # Initialize conversation metadata.

    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    if "created_at" not in st.session_state:
        st.session_state.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = DEFAULT_MODEL

    # Initialize clear chat dialog state.

    if "clear_chat_confirmed" not in st.session_state:
        st.session_state.clear_chat_confirmed = False
