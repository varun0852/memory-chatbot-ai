"""
Logout component.
"""

import streamlit as st


def logout_button() -> None:
    """
    Logout the current user.
    """

    st.sidebar.divider()

    st.sidebar.markdown("### 👤 Logged in as")
    st.sidebar.success(st.session_state.username)

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True,
    ):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None

        st.session_state.messages = []

        st.rerun()