"""
Document Section Component.

Handles PDF upload and management.
"""

import streamlit as st

from backend.document import DocumentProcessor

from utils.document_session import clear_document


def render_document_section() -> None:
    """
    Render the document upload section.
    """

    st.markdown("### 📄 Document")

    uploaded_pdf = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        help="Upload a PDF to chat with its content.",
    )

    if uploaded_pdf and uploaded_pdf.name != st.session_state.document_name:

        processor = DocumentProcessor()

        st.session_state.document_text = processor.extract_text(uploaded_pdf)

        st.session_state.document_name = uploaded_pdf.name

        st.success("✅ PDF uploaded successfully.")

    if st.session_state.document_name:

        st.info(f"📄 Current document: {st.session_state.document_name}")

        if st.button(
            "🗑 Remove Document",
            use_container_width=True,
        ):

            clear_document()

            st.success("Document removed successfully.")

            st.rerun()

        st.caption(f"Extracted {len(st.session_state.document_text):,} characters.")
