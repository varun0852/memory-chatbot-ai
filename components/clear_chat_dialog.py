import streamlit as st


@st.dialog("🗑️ Clear Conversation")
def clear_chat_dialog() -> bool:
    """
    Display a confirmation dialog before clearing the chat.

    Returns:
        True if the user confirms, otherwise False.
    """

    st.warning(
        "Are you sure you want to clear the current conversation?\n\n"
        "This action cannot be undone."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Cancel",
            use_container_width=True,
        ):
            st.rerun()

    with col2:
        if st.button(
            "Clear Chat",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.clear_chat_confirmed = True
            st.rerun()
            