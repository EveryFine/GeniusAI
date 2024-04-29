# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     home.py
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

import hmac

import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Genius Chatbots",
    page_icon="🤖",
)





def login(config):
    with open(config) as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    authenticator.login()
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    return authenticator


authenticator = login('.streamlit/config.yaml')
if st.session_state["authentication_status"]:
    st.sidebar.title("💬Genius Chatbots")
    st.title('💬Genius Chatbots')
    """
    Nice to meet you!! 🤝 This is a genius chatbots community to assist human daily life and working.
    Please enjoy it! 💯
    """
