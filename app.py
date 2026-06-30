import streamlit as st

from backend import ChatBot

import logging

logger = logging.getLogger(__name__)


st.set_page_config(page_title = "Memory ChatBot")

st.title("🧠 Memory ChatBot")

st.caption("Powered by Google Gemini")

with st.expander("ℹ️ About This Project"):
    st.markdown("""
### 🧠 Memory ChatBot

A conversational AI chatbot built using **Google Gemini** and **Streamlit**.

### 🚀 Features

- 💬 Multi-turn conversations
- 🧠 Conversation memory
- 🤖 Google Gemini integration
- 🏗️ Object-Oriented architecture
- 🔒 Secure API key management
- 🧪 Backend testing

### 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API

**Version:** 1.0

---
👨‍💻 Built by **Varun**
""")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Google Gemini API Key",type="password",help="Leave empty to use the key stored in your .env file.")

    if not api_key:
        st.info("Using API key from .env if available.")
    st.markdown("[Get your API key here](https://aistudio.google.com/app/apikey)")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

        if "chatbot" in st.session_state:
            del st.session_state.chatbot

        st.rerun()

    st.sidebar.divider()

    st.sidebar.markdown("""
    ### 👨‍💻 Created by Varun

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

Built to demonstrate conversational AI with memory using Google's Gemini API.

✨ Features:
• Multi-turn conversation
• Conversation memory
• Clean OOP architecture
• Google Gemini integration

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

                    response_text = st.session_state.chatbot.chat(prompt, st.session_state.messages)
                    st.markdown(response_text)


                    st.session_state.messages.append({"role": "assistant" , "content" : response_text})
                except Exception as e:
                    logger.exception("Unexpected error while generating response.")

                    st.error(
                        "Something went wrong while generating the response."
                    )
    else:
        st.error("Please enter a valid API Key to initialize the chatbot.")


st.divider()

st.markdown("""
<div style="text-align:center; color:gray; font-size:14px;">
👨‍💻 <b>Created by Varun</b><br>
AI Engineer • Generative AI
</div>
""", unsafe_allow_html=True)

