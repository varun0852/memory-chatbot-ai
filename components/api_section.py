"""
API Section Component.

Renders the API key configuration.
"""

import streamlit as st


def render_api_section() -> str:
    """
    Render the API key section.

    Returns:
        API key entered by the user.
    """
    st.markdown("### 🔑 API Access")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Leave empty to use the Groq API key stored in your .env file.",
    )

    if not api_key:
        st.info("Using API key from .env if available.")
    st.markdown("[Get your Groq API key](https://console.groq.com/keys)")

    return api_key
