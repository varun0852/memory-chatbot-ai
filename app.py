import streamlit as st

from backend import ChatBot

from datetime import datetime

from utils.chat_utils import generate_session_id

from config import APP_TITLE, AUTHOR, APP_VERSION

from utils.exporter import export_as_text, export_as_markdown

from utils.pdf_exporter import export_as_pdf

from utils.validator import validate_prompt

from backend.exceptions import (
    InvalidAPIKeyError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    ResponseError
)

from models import ChatMessage, ConversationMetadata

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="centered",
)

st.title(f"🧠 {APP_TITLE}")

st.caption("Powered by AI")

# Initialize session state variables       

if "messages" not in st.session_state:
    st.session_state.messages = []

# Generate a unique session ID for the conversation    

if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()

# Metadata used by export features

metadata = ConversationMetadata = {
    "conversation_id": st.session_state.session_id,
    "exported_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

with st.expander("ℹ️ About This Project"):
    st.markdown(f"""
### 🧠 Memory ChatBot

A conversational AI chatbot built using **Groq**, **Llama 3.3 70B**, and **Streamlit**.

### 🚀 Features

- 💬 Multi-turn conversations
- 🧠 Conversation memory
- 🤖 LLM integration
- 🏗️ Object-Oriented architecture
- 🔒 Secure API key management
- 🧪 Backend testing

### 🛠️ Tech Stack

- Python
- Streamlit
- LLM API

f**Version:** v{APP_VERSION}

---
👨‍💻 Built by **{AUTHOR}**
""")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key",type="password",help="Leave empty to use the Groq API key stored in your .env file.")

    if not api_key:
        st.info("Using API key from .env if available.")
    st.markdown("[Get your Groq API key](https://console.groq.com/keys)")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

        if "chatbot" in st.session_state:
            del st.session_state.chatbot
        
         # Generate a new conversation ID
        st.session_state.session_id = generate_session_id()


        st.rerun()

    st.sidebar.divider()

    # Export conversation
    st.markdown("### 📤 Export Conversation")

    st.info(
        "Download the current conversation in different formats."
    )

    # Check whether there are any messages to export
    has_messages = len(st.session_state.messages) > 0


# Export conversation as TEXT file
    txt_content = export_as_text(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label = "📄 Download TXT",
        data = txt_content,
        file_name = f"{metadata['conversation_id']}.txt",
        mime = "text/plain",
        disabled = not has_messages
    )

# Export conversation as MARKDOWN file
    markdown_content = export_as_markdown(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label = "📝 Download Markdown",
        data = markdown_content,
        file_name = f"{metadata['conversation_id']}.md",
        mime = "text/markdown",
        disabled = not has_messages
    )

    # Export conversation as PDF file
    pdf_content = export_as_pdf(
        st.session_state.messages,
        metadata,
    )

    st.download_button(
        label = "📕 Download PDF",
        data = pdf_content,
        file_name = f"{metadata['conversation_id']}.pdf",
        mime = "application/pdf",
        disabled = not has_messages
    )

    if not has_messages:
        st.caption("💡 Start a conversation to enable exporting")

    # Display conversation ID

    st.sidebar.markdown("### 💬 Conversation")

    st.sidebar.code(st.session_state.session_id)

    st.sidebar.markdown(f"""
    ### 👨‍💻 Created by {AUTHOR}

    AI Engineer • Generative AI
    """)

# Initialize ChatBot instance

if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = ChatBot(api_key)
    except InvalidAPIKeyError as e:
        st.error(str(e))


# Welcome screen

if not st.session_state.messages:
    st.info("""
👋 Welcome to Memory ChatBot

Built to demonstrate conversational AI with memory using Groq's Llama 3.3 model.

✨ Features:
• Multi-turn conversation
• Conversation memory
• Clean OOP architecture
• Groq LLM integration

How can I help you today?"""
)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


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
            with st.spinner("🤖 Thinking..."):
                try:
                    response_text = st.session_state.chatbot.chat(
                        prompt,
                        st.session_state.messages
                    )

                    st.markdown(response_text)

                    assistant_message: ChatMessage = {
                            "role": "assistant",
                            "content": response_text,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                        }
                    
                    st.session_state.messages.append(assistant_message)
                    
                    # Refresh the UI so the latest conversation state is displayed.
                    st.rerun()

                except InvalidAPIKeyError as e:
                    st.error(f"🔑 {e}")

                except APIConnectionError as e:
                    st.error(f"🌐 {e}")

                except APITimeoutError as e:
                    st.error(f"⏳ {e}")

                except RateLimitError as e:
                    st.error(f"🚦 {e}")

                except ResponseError as e:
                    st.error(f"🤖 {e}")

                except Exception as e:
                    st.exception(e)
                


st.divider()

st.markdown(f"""
<div style="text-align:center; color:gray; font-size:14px;">
👨‍💻 <b>{AUTHOR}</b><br>
AI Engineer • Generative AI
</div>
""", unsafe_allow_html=True)

