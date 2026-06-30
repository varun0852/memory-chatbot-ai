import streamlit as st
import backend as logic


st.set_page_config(page_title = "Gemini LangChain Chatbot")

st.title("Gemini ChatBot With Memory")


with st.sidebar:
    st.header("setting")
    api_key = st.text_input("Enter Google API Key:" , type = "password")
    if not api_key:
        st.warning("please enter your API key to proceed.")
    st.markdown("[Get your API key here] (https://aistudio.google.com/app/apikey)")


if "chain" not in st.session_state and api_key:
    st.session_state.chain = logic.initialize_gemini_chain(api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("what is on your mind?"):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role" : "user" , "content" : prompt})


    if st.session_state.get("chain"):
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:

                    response_text = logic.get_chatbot_response(st.session_state.chain, prompt)
                    st.markdown(response_text)


                    st.session_state.messages.append({"role": "assistant" , "content" : "response_text"})
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a valid API Key to initialize the chatbot.")

