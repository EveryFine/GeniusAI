# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     bot_b
   Description :
   Author :       EveryFine
   Date：          2024/4/27
-------------------------------------------------
   Change Activity:
                   2024/4/27:
   Product:       PyCharm
-------------------------------------------------
"""
__author__ = 'EveryFine'

import streamlit as st

from home import login


def create_chatbot():
    st.title('Chatbot Type B')
    st.write('This is the page for Chatbot Type B.')
    user_input = st.text_input("Say something to Bot B")
    if user_input:
        st.write(f"Bot B says: I received your message: {user_input}")


login('.streamlit/config.yaml')
if st.session_state["authentication_status"]:
    create_chatbot()

