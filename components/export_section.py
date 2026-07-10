"""
Export Section Component.

Renders all conversation export options.
"""

import streamlit as st

from database.conversation_db import ConversationDatabase

from models import ConversationMetadata

from utils.exporter import (
    export_as_markdown,
    export_as_text,
)

from utils.pdf_exporter import export_as_pdf

from utils.share import export_chat_package


def render_export_section(
    db: ConversationDatabase,
    metadata: ConversationMetadata,
) -> None:
    """
    Render the conversation export section.

    Provides download options for the current conversation
    in TXT, Markdown, PDF, and portable .chat package
    formats. Export statistics are updated after each
    successful download.
    """

    st.markdown("### 📤 Export")

    st.info("Download the current conversation in different formats.")
    chat_package = export_chat_package(
        st.session_state.messages,
        metadata,
    )
    # ==========================================================
    # Check whether there are any messages to export
    # ==========================================================

    has_messages = len(st.session_state.messages) > 0

    # Export as TXT

    txt_content = export_as_text(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label="📄 Download TXT",
        data=txt_content,
        file_name=f"{metadata['conversation_id']}.txt",
        mime="text/plain",
        disabled=not has_messages,
        on_click=db.increment_export_count,
        args=(
            st.session_state.user_id,
            st.session_state.session_id,
        ),
    )
    # Export as Markdown

    markdown_content = export_as_markdown(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label="📝 Download Markdown",
        data=markdown_content,
        file_name=f"{metadata['conversation_id']}.md",
        mime="text/markdown",
        disabled=not has_messages,
        on_click=db.increment_export_count,
        args=(
            st.session_state.user_id,
            st.session_state.session_id,
        ),
    )
    # Export as PDF

    pdf_content = export_as_pdf(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label="📕 Download PDF",
        data=pdf_content,
        file_name=f"{metadata['conversation_id']}.pdf",
        mime="application/pdf",
        disabled=not has_messages,
        on_click=db.increment_export_count,
        args=(
            st.session_state.user_id,
            st.session_state.session_id,
        ),
    )

    if not has_messages:
        st.caption("💡 Start a conversation to enable exporting")

    # Export as .chat package

    st.download_button(
        label="📦 Export Conversation Package",
        data=chat_package,
        file_name=(f"memory_chat_" f"{metadata['conversation_id']}.chat"),
        mime="application/json",
        disabled=not has_messages,
        on_click=db.increment_export_count,
        args=(
            st.session_state.user_id,
            st.session_state.session_id,
        ),
    )
