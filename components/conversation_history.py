"""
Conversation History Component.

Displays saved conversations in the sidebar.
"""

from datetime import date
from datetime import datetime

import streamlit as st

from database.conversation_db import ConversationDatabase
from utils.session import reset_chat_session


def render_conversation_history(
    db: ConversationDatabase,
) -> None:
    """
    Render the conversation history section.

    Displays saved conversations, supports searching,
    loading, and deleting conversations, and highlights
    the currently active conversation.
    """

    search_query = st.text_input(
        "Search conversations",
        placeholder="Search...",
    )

    if search_query:
        conversations = db.search_conversations(search_query)
    else:
        conversations = db.get_conversations()

    if not conversations:
        if search_query:
            st.info("🔍 No conversations found.")
        else:
            st.caption("No saved conversations.")

    else:
        last_date = None

        for session_id, title, created_at in conversations:

            display_title = title[:30] + "..." if len(title) > 30 else title

            conversation_date = datetime.strptime(
                created_at,
                "%Y-%m-%d %H:%M:%S",
            )

            today = date.today()

            if conversation_date.date() == today:
                date_label = "Today"
            else:
                date_label = conversation_date.strftime("%b %d")

            # Render the date header only once for each date group.
            if last_date != date_label:
                st.caption(f"📅 {date_label}")
                last_date = date_label

            # Create the row AFTER rendering the date header
            col1, col2 = st.columns([6, 0.8])

            label = display_title

            if session_id == st.session_state.session_id:
                label = f"🟢 {display_title}"

            with col1:
                if st.button(
                    label,
                    key=f"load_{session_id}",
                    use_container_width=True,
                ):
                    st.session_state.messages = db.load_conversation(session_id)

                    st.session_state.session_id = session_id

                    st.rerun()

            with col2:
                if st.button(
                    "🗑",
                    key=f"delete_{session_id}",
                    use_container_width=True,
                ):
                    db.delete_conversation(session_id)

                    if session_id == st.session_state.session_id:
                        reset_chat_session()

                    st.rerun()
