"""
Import Section Component.

Handles importing conversation packages.
"""

from datetime import datetime

import streamlit as st

from database.conversation_db import ConversationDatabase

from utils.chat_utils import generate_session_id

from utils.share import import_chat_package


def render_import_section(
    db: ConversationDatabase,
) -> None:
    """
    Render the conversation import section.
    """

    st.markdown("### 📥 Import")

    uploaded_chat = st.file_uploader(
        "Import Conversation Package (.chat)",
        type=["chat"],
        key=f"chat_import_{st.session_state.import_key}",
        help=("Import a previously exported " "Memory ChatBot conversation."),
    )

    if uploaded_chat:

        st.info(f"📄 Selected file: {uploaded_chat.name}")

        import_clicked = st.button(
            "📥 Import Conversation",
            use_container_width=True,
        )

        if import_clicked:

            try:

                package = uploaded_chat.read().decode("utf-8")

                messages, metadata = import_chat_package(package)

                # Restore conversation
                st.session_state.messages = messages

                # Generate a NEW session ID
                st.session_state.session_id = generate_session_id()

                # Restore original creation time if available
                st.session_state.created_at = metadata.get(
                    "created_at",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

                # Save imported conversation
                db.save_conversation(
                    session_id=st.session_state.session_id,
                    title=messages[0]["content"][:50],
                    created_at=st.session_state.created_at,
                    messages=messages,
                )

                st.session_state.show_import_success = True

                st.session_state.import_key += 1

                st.rerun()

            except ValueError as e:

                st.error(str(e))

            except Exception as e:

                st.exception(e)
