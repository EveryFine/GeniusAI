# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     bot_a
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

import os

import streamlit as st
from langchain_community.llms.openai import OpenAI
from langchain_core.messages import AIMessage, HumanMessage

from home import login
from llm_clients.openai_client import OpenAIClient

st.set_page_config(page_title="A Class Chatbot", page_icon="🦤")


def create_chatbot():
    global st
    model_name = "gpt-3.5-turbo"
    # model_name = "gpt-4o"
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm_client = OpenAIClient(model_name=model_name, openai_api_key=openai_api_key)
    st.sidebar.header("🦤 A Class Chatbot")
    st.markdown("# 🦤 A Class Chatbot")
    st.markdown(
        """
        #### This an A class chatbot to assist the human resolve some simple issues!🥰
        > It is a little for this chatbot to answer about real-time information such as the current date
        
        """
    )
    # session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am A class bot. How can I help you?"),
        ]
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != '':
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            response = st.write_stream(llm_client.get_stream_response(user_query, st.session_state.chat_history))
        st.session_state.chat_history.append(AIMessage(content=response))


login('.streamlit/config.yaml')
if st.session_state["authentication_status"]:
    create_chatbot()
