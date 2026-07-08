"""
Footer component.

Displays the application footer.
"""

import streamlit as st

from config import AUTHOR


def render_footer() -> None:
    """
    Render the application footer.
    """

    st.divider()

    st.markdown(
        f"""
<div style="text-align:center; color:gray; font-size:14px;">
👨‍💻 <b>{AUTHOR}</b><br>
AI Engineer • Generative AI
</div>
""",
        unsafe_allow_html=True,
    )
