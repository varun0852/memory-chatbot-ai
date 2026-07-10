import uuid

import streamlit as st
from streamlit_cookies_controller import CookieController

COOKIE_NAME = "memory_chatbot_user_id"

controller = CookieController()


def get_user_id():
    cookies = controller.getAll()

    st.sidebar.write("Cookies:", cookies)

    user_id = controller.get(COOKIE_NAME)

    st.sidebar.write("Current user_id:", user_id)

    if user_id:
        return user_id

    user_id = str(uuid.uuid4())

    st.sidebar.write("Generated:", user_id)

    controller.set(COOKIE_NAME, user_id)

    return user_id