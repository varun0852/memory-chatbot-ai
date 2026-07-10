"""
Authentication UI.
"""

import streamlit as st

from database.user_db import UserDatabase


db = UserDatabase()


def login_page() -> None:
    """
    Render the login page.
    """

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password",
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Login",
            use_container_width=True,
        ):

            user_id = db.authenticate_user(
                username,
                password,
            )

            if user_id:

                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username

                st.rerun()

            st.error("Invalid username or password.")

    with col2:

        if st.button(
            "Login as Demo",
            use_container_width=True,
        ):

            user_id = db.authenticate_user(
                "demo",
                "demo123",
            )

            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.username = "demo"

            st.rerun()

    st.divider()

    st.subheader("Create Account")

    new_username = st.text_input(
        "New Username"
    )

    new_password = st.text_input(
        "New Password",
        type="password",
    )

    if st.button(
        "Create Account",
        use_container_width=True,
    ):

        success = db.create_user(
            new_username,
            new_password,
        )

        if success:

            st.success(
                "Account created successfully. Please log in."
            )

        else:

            st.error(
                "Username already exists."
            )