import streamlit as st


def clear_document() -> None:
    """
    Remove the currently uploaded document from the session.
    """

    st.session_state.document_text = None
    st.session_state.document_name = None