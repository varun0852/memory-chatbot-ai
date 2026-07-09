"""
Welcome component.

Displays the welcome screen when no conversation exists.
"""

import streamlit as st

from config import APP_TITLE


def render_welcome() -> None:
    """
    Render the application welcome screen.

    Displays an introduction and feature overview when
    the current conversation is empty.
    """

    if st.session_state.messages:
        return

    st.info(f"""
# 👋 Welcome to {APP_TITLE}

An intelligent conversational AI assistant built to demonstrate modern AI engineering practices.

### ✨ Features

- 💬 Multi-turn conversations
- 🧠 Conversation memory
- ⚡ Streaming responses
- 🤖 AI model selection
- 📄 Export conversations (TXT, Markdown & PDF)
- 📦 Import & Export conversation packages
- 🔒 Secure API key support

---

Start chatting below to begin your conversation.
""")
