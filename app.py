"""
Memory ChatBot AI.

Main Streamlit application entry point.

Coordinates application initialization,
sidebar components, chat interaction,
conversation management, and rendering.
"""

# Standard Library
from datetime import datetime

# Third-Party
import streamlit as st

# Backend
from backend import ChatBot
from backend.exceptions import (
    InvalidAPIKeyError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    ResponseError,
)

# Components
from components.model_selector import render_model_selector
from components.clear_chat_dialog import clear_chat_dialog
from components.analytics import render_analytics
from components.welcome import render_welcome
from components.footer import render_footer
from components.auth import login_page
from components.logout import logout_button
from components.conversation_history import (
    render_conversation_history,
)
from components.export_section import (
    render_export_section,
)
from components.import_section import (
    render_import_section,
)
from components.document_section import (
    render_document_section,
)

# Configuration
from config import (
    APP_TITLE,
    APP_VERSION,
    AUTHOR,
)

# Models
from models import ChatMessage, ConversationMetadata

# Utilities
from utils.session import reset_chat_session
from utils.validator import validate_prompt
from components.api_section import (
    render_api_section,
)
from utils.session_initializer import (
    initialize_session_state,
)


from database.conversation_db import ConversationDatabase

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title(f"🧠 {APP_TITLE}")

st.caption("Modern Conversational AI")

# ==========================================================
# Initialize session state variables
# ==========================================================

initialize_session_state()

if not st.session_state.logged_in:
    login_page()
    st.stop()

logout_button()


if st.session_state.show_import_success:

    st.toast(
        "Conversation imported successfully!",
        icon="✅",
    )

    st.session_state.show_import_success = False

# ==========================================================
# Initialize Database
# ==========================================================

db = ConversationDatabase()

# ==========================================================
# Metadata used by export features
# ==========================================================

metadata: ConversationMetadata = {
    "conversation_id": st.session_state.session_id,
    "created_at": st.session_state.created_at,
    "exported_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "model": st.session_state.selected_model,
}

with st.expander("ℹ️ About Memory ChatBot AI"):
    st.markdown(f"""
# 🧠 Memory ChatBot AI

A production-quality conversational AI application built to demonstrate modern AI engineering practices.

---

## ✨ Features

- 💬 Multi-turn conversations
- 🧠 Persistent conversation memory
- ⚡ Real-time streaming responses
- 🤖 AI model selection
- 📄 Export conversations to TXT, Markdown, and PDF
- 🔒 Secure API key management
- 🛡️ Robust error handling and retry logic
- 📝 Session management

---

## 🛠️ Technology Stack

- 🐍 Python
- 🎈 Streamlit
- 🤖 Large Language Models (LLMs)
- 🏗️ Object-Oriented Architecture
- 📦 Modular Project Structure

---

## 🎯 Project Goals

This project is designed to showcase production-ready AI application development, including clean architecture, maintainable code, and an intuitive user experience.

---

**Version:** v{APP_VERSION}

👨‍💻 **Developed by {AUTHOR}**
""")

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.header("⚙️ Settings")

    st.markdown("### 🤖 AI Model")

    new_model = render_model_selector(st.session_state.selected_model)

    if new_model:

        st.session_state.selected_model = new_model

        reset_chat_session()

        st.success("✅ Model changed successfully.")

        st.rerun()

    st.divider()

    render_document_section()

    st.divider()
    api_key = render_api_section()

    st.divider()
    st.markdown("### 🗑️ Conversation")

    if st.button("🗑️ Clear Chat"):
        clear_chat_dialog()

    if st.session_state.clear_chat_confirmed:
        reset_chat_session()
        st.session_state.clear_chat_confirmed = False
        st.rerun()

    st.sidebar.divider()

    st.divider()

    st.markdown("### 💬 Conversation History")

    render_conversation_history(db)

    # ==========================================================
    # Conversation analytics
    # ==========================================================

    statistics = db.get_statistics(
        st.session_state.user_id,
    )
    render_analytics(statistics)

    # ==========================================================
    # Export conversation and Import conversation
    # ==========================================================

    st.divider()
    render_export_section(
        db=db,
        metadata=metadata,
    )

    # ==========================================================
    # Import conversation package (.chat)
    # ==========================================================

    st.divider()

    render_import_section(
        db=db,
    )
    # ==========================================================
    # Display conversation ID
    # ==========================================================

    st.divider()
    st.markdown("### 💬 Session")

    st.sidebar.code(st.session_state.session_id)

    st.divider()

    st.markdown(f"""
    ### 👨‍💻 About

    **{AUTHOR}**

    AI Engineer • Generative AI
    """)

# ==========================================================
# Initialize ChatBot instance
# ==========================================================


if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = ChatBot(
            api_key=api_key,
            model=st.session_state.selected_model,
        )
    except InvalidAPIKeyError as e:
        st.error(str(e))


# ==========================================================
# Welcome screen
# ==========================================================

render_welcome()


# ==========================================================
# Display Conversation
# ==========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# Handle User Input
# ==========================================================

if prompt := st.chat_input("What would you like to talk about?"):

    try:
        validate_prompt(prompt)

    except ValueError as e:
        st.warning(str(e))
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)

    user_message: ChatMessage = {
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }

    st.session_state.messages.append(user_message)

    if st.session_state.get("chatbot"):
        with st.chat_message("assistant"):
            with st.status(
                "🤖 Generating response...",
                expanded=True,
            ) as status:
                try:
                    status.write("🧠 Preparing conversation...")

                    if st.session_state.document_text:
                        status.write("📄 Adding document content...")

                    status.write("🌐 Contacting AI model...")

                    response_text = st.write_stream(
                        st.session_state.chatbot.stream_chat(
                            user_message=prompt,
                            history=st.session_state.messages,
                            document_text=st.session_state.document_text,
                        )
                    )

                    assistant_message: ChatMessage = {
                        "role": "assistant",
                        "content": response_text,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                    }

                    status.write("✍️ Finalizing response...")

                    status.update(
                        label="✅ Response generated successfully!",
                        state="complete",
                        expanded=False,
                    )

                    st.session_state.messages.append(assistant_message)

                    db.save_conversation(
                        user_id=st.session_state.user_id,
                        session_id=st.session_state.session_id,
                        title=st.session_state.messages[0]["content"][:50],
                        created_at=st.session_state.created_at,
                        messages=st.session_state.messages,
                    )

                    # Refresh UI

                    st.rerun()

                except InvalidAPIKeyError as e:

                    status.update(
                        label="❌ Failed to generate response.",
                        state="error",
                        expanded=True,
                    )

                    st.error(f"🔑 {e}")

                except APIConnectionError as e:

                    status.update(
                        label="❌ Failed to generate response.",
                        state="error",
                        expanded=True,
                    )

                    st.error(f"🌐 {e}")

                except APITimeoutError as e:

                    status.update(
                        label="❌ Failed to generate response.",
                        state="error",
                        expanded=True,
                    )

                    st.error(f"⏳ {e}")

                except RateLimitError as e:

                    status.update(
                        label="❌ Failed to generate response.",
                        state="error",
                        expanded=True,
                    )

                    st.error(f"🚦 {e}")

                except ResponseError as e:

                    status.update(
                        label="❌ Failed to generate response.",
                        state="error",
                        expanded=True,
                    )

                    st.error(f"🤖 {e}")

                except Exception as e:

                    status.update(
                        label="❌ Failed to generate response.",
                        state="error",
                        expanded=True,
                    )

                    st.exception(e)


# ==========================================================
# Footer
# ==========================================================

render_footer()
