# Standard Library
from datetime import datetime, date

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
from backend.document import DocumentProcessor

# Components
from components.model_selector import render_model_selector
from components.clear_chat_dialog import clear_chat_dialog
from components.analytics import render_analytics , render_current_session

# Configuration
from config import (
    APP_TITLE,
    APP_VERSION,
    AUTHOR,
    DEFAULT_MODEL,
)

# Models
from models import ChatMessage, ConversationMetadata

# Utilities
from utils.chat_utils import generate_session_id
from utils.exporter import export_as_markdown, export_as_text
from utils.pdf_exporter import export_as_pdf
from utils.session import reset_chat_session
from utils.validator import validate_prompt
from utils.document_session import clear_document
from utils.share import (
    export_chat_package,
    import_chat_package,
)


from database.conversation_db import ConversationDatabase


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="centered",
)

st.title(f"🧠 {APP_TITLE}")

st.caption("Modern Conversational AI")

# ==========================================================
# Initialize session state variables    
# ==========================================================   

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_text" not in st.session_state:
    st.session_state.document_text = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "import_key" not in st.session_state:
    st.session_state.import_key = 0

if "show_import_success" not in st.session_state:
    st.session_state.show_import_success = False


# ==========================================================
# Generate a unique session ID for the conversation    
# ==========================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()

if "created_at" not in st.session_state:
    st.session_state.created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

if "selected_model" not in st.session_state:
    st.session_state.selected_model = DEFAULT_MODEL

# ==========================================================
# Generate a Dialog for clear conversation    
# ==========================================================

if "clear_chat_confirmed" not in st.session_state:
    st.session_state.clear_chat_confirmed = False


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
    "exported_on": datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
        ),
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

    new_model = render_model_selector(
        st.session_state.selected_model
    )

    if new_model:

        st.session_state.selected_model = new_model

        reset_chat_session()

        st.success("✅ Model changed successfully.")

        st.rerun()

    st.divider()
    st.markdown("### 📄 Document")

    uploaded_pdf = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        help="Upload a PDF to chat with its content.",
    )

    if (
        uploaded_pdf
        and uploaded_pdf.name != st.session_state.document_name
    ):

        processor = DocumentProcessor()

        st.session_state.document_text = (
            processor.extract_text(uploaded_pdf)
            )

        st.session_state.document_name = uploaded_pdf.name

        st.success("✅ PDF uploaded successfully.")

    if st.session_state.document_name:

        st.info(
            f"📄 Current document: {st.session_state.document_name}"
        )

        if st.button(
            "🗑 Remove Document",
            use_container_width=True,
        ):

            clear_document()

            st.success("Document removed successfully.")

            st.rerun()

        st.caption(
            f"Extracted {len(st.session_state.document_text):,} characters."
        )

    st.divider()
    st.markdown("### 🔑 API Access")   

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Leave empty to use the Groq API key stored in your .env file.",
    )

    if not api_key:
        st.info("Using API key from .env if available.")
    st.markdown("[Get your Groq API key](https://console.groq.com/keys)")


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

            display_title = (
                title[:30] + "..."
                if len(title) > 30
                else title
            )

            conversation_date = datetime.strptime(
                created_at,
                "%Y-%m-%d %H:%M:%S",
            )

            today = date.today()

            if conversation_date.date() == today:
                date_label = "Today"
            else:
                date_label = conversation_date.strftime("%b %d")

            # Show the date only once for each group
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
                    st.session_state.messages = db.load_conversation(
                        session_id
                    )

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

# ==========================================================
# Conversation analytics
# ==========================================================

        statistics = db.get_statistics()
        render_analytics(statistics)

# ==========================================================
# Export conversation and Import conversation
# ==========================================================

    st.divider()
    st.markdown("### 📤 Export")

    st.info(
        "Download the current conversation in different formats."
    )    
    chat_package = export_chat_package(
        st.session_state.messages,
        metadata,
    )
# ==========================================================
# Check whether there are any messages to export
# ==========================================================

    has_messages = len(st.session_state.messages) > 0

# ==========================================================
# Export conversation as TEXT file
# ==========================================================

    txt_content = export_as_text(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label = "📄 Download TXT",
        data = txt_content,
        file_name = f"{metadata['conversation_id']}.txt",
        mime = "text/plain",
        disabled = not has_messages,
        on_click=db.increment_export_count,
        args=(st.session_state.session_id,),

    )
# ==========================================================
# Export conversation as MARKDOWN file
# ==========================================================

    markdown_content = export_as_markdown(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label = "📝 Download Markdown",
        data = markdown_content,
        file_name = f"{metadata['conversation_id']}.md",
        mime = "text/markdown",
        disabled = not has_messages,
        on_click=db.increment_export_count,
        args=(st.session_state.session_id,),
    )
# ==========================================================
# Export conversation as PDF file
# ==========================================================

    pdf_content = export_as_pdf(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label = "📕 Download PDF",
        data = pdf_content,
        file_name = f"{metadata['conversation_id']}.pdf",
        mime = "application/pdf",
        disabled = not has_messages,
        on_click=db.increment_export_count,
        args=(st.session_state.session_id,),
    )

    if not has_messages:
        st.caption("💡 Start a conversation to enable exporting")

# ==========================================================
# Export conversation package (.chat) 
# ==========================================================

    st.download_button(
        label="📦 Export Conversation Package",
        data=chat_package,
        file_name=(
            f"memory_chat_"
            f"{metadata['conversation_id']}.chat"
        ),
        mime="application/json",
        disabled=not has_messages,
        on_click=db.increment_export_count,
        args=(st.session_state.session_id,),
    )

# ==========================================================
# Import conversation package (.chat)
# ==========================================================

    st.divider()

    st.markdown("### 📥 Import")

    uploaded_chat = st.file_uploader(
        "Import Conversation Package (.chat)",
        type=["chat"],
        key=f"chat_import_{st.session_state.import_key}",
        help=(
            "Import a previously exported "
            "Memory ChatBot conversation."
        ),
    )

    if uploaded_chat:

        st.info(f"📄 Selected file: {uploaded_chat.name}")

        import_clicked = st.button(
            "📥 Import Conversation",
            use_container_width=True,
        )

        if import_clicked:

            try:

                package = (
                    uploaded_chat.read()
                    .decode("utf-8")
                )

                messages, metadata = import_chat_package(
                    package
                )

                # Restore conversation
                st.session_state.messages = messages

                # Generate a NEW session ID
                st.session_state.session_id = (
                    generate_session_id()
                )

                # Restore original creation time if available
                st.session_state.created_at = metadata.get(
                    "created_at",
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
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

if not st.session_state.messages:
    st.info(f"""
    # 👋 Welcome to {APP_TITLE}

    An intelligent conversational AI assistant built to demonstrate modern AI engineering practices.

    ### ✨ Features

    - 💬 Multi-turn conversations
    - 🧠 Conversation memory
    - ⚡ Streaming responses
    - 🤖 AI model selection
    - 📄 Export conversations (TXT, Markdown & PDF)
    - 🔒 Secure API key support

    ---

    Start chatting below to begin your conversation.
    """)

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
            "role" : "user",
            "content" : prompt,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
    
    st.session_state.messages.append(user_message)



    if st.session_state.get("chatbot"):
        with st.chat_message("assistant"):
            with st.status(
                "🤖 Generating response...",
                expanded=True,
            ) as status : 
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

st.divider()

st.markdown(f"""
<div style="text-align:center; color:gray; font-size:14px;">
👨‍💻 <b>{AUTHOR}</b><br>
AI Engineer • Generative AI
</div>
""", unsafe_allow_html=True)

