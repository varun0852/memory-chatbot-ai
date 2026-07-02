import streamlit as st

from backend import ChatBot

from config import APP_TITLE, AUTHOR


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="centered",
)

st.title(f"🧠 {APP_TITLE}")

st.caption("Powered by AI")

with st.expander("ℹ️ About This Project"):
    st.markdown(f"""
### 🧠 Memory ChatBot

A conversational AI chatbot built using **Groq**, **Llama 3.3 70B**, and **Streamlit**.

### 🚀 Features

- 💬 Multi-turn conversations
- 🧠 Conversation memory
- 🤖 Groq LLM integration
- 🏗️ Object-Oriented architecture
- 🔒 Secure API key management
- 🧪 Backend testing

### 🛠️ Tech Stack

- Python
- Streamlit
- Groq API

**Version:** 1.1

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

        st.rerun()

    st.sidebar.divider()

    st.sidebar.markdown(f"""
    ### 👨‍💻 Created by {AUTHOR}

    AI Engineer • Generative AI
    """)


if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = ChatBot(api_key)
    except ValueError as e:
        st.error(str(e))

if "messages" not in st.session_state:
    st.session_state.messages = []

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

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role" : "user" , "content" : prompt})


    if st.session_state.get("chatbot"):
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    response_text = st.session_state.chatbot.chat(
                        prompt,
                        st.session_state.messages
                    )

                    st.markdown(response_text)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response_text
                        }
                    )

                except Exception as e:
                    st.error(f"⚠️ Unexpected error: {e}")
                


st.divider()

st.markdown(f"""
<div style="text-align:center; color:gray; font-size:14px;">
👨‍💻 <b>{AUTHOR}</b><br>
AI Engineer • Generative AI
</div>
""", unsafe_allow_html=True)

