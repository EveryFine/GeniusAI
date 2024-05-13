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

import os

import streamlit as st
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.runnables import RunnableConfig

from home import login
from llm_clients.openai_chat_agent import OpenAIChatAgent

# 解决错误：RuntimeError: There is no current event loop in thread 'ScriptRunner.scriptThread'.
import asyncio

# def get_or_create_eventloop():
#     try:
#         return asyncio.get_event_loop()
#     except RuntimeError as ex:
#         if "There is no current event loop in thread" in str(ex):
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             return asyncio.get_event_loop()
#
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)

st.set_page_config(page_title="B Class Chatbot", page_icon="🐇")



def create_chatbot():
    st.sidebar.header("🐇B Class Chatbot")
    st.markdown("# 🐇B Class Chatbot")
    st.markdown(
        """
        #### This a B class chatbot to assist the human resolve some comprehensive issues!🥰
        > He can use the tools to find the answer of the question by himself.

        """
    )
    model_name = "gpt-3.5-turbo"
    openai_api_key = os.getenv("OPENAI_API_KEY")
    msgs = StreamlitChatMessageHistory()
    memory = ConversationBufferMemory(
        chat_memory=msgs,
        return_messages=True,
        memory_key="chat_history",
        output_key="output"
    )
    if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
        msgs.clear()
        msgs.add_ai_message("How can I help you?")
        st.session_state.steps = {}
    avatars = {"human": "user", "ai": "assistant"}
    for idx, msg in enumerate(msgs.messages):
        with st.chat_message(avatars[msg.type]):
            for step in st.session_state.steps.get(str(idx), []):
                if step[0].tool == "_Exception":
                    continue
                with st.status(f"**{step[0].tool}**: {step[0].tool_input}", state="complete"):
                    st.write(step[0].log)
                    st.write(step[1])
            st.write(msg.content)

    if prompt := st.chat_input("Who won the women's U.S. Open in 2018?"):
        st.chat_message("user").write(prompt)
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        tools = [TavilySearchResults()]
        chat_agent = OpenAIChatAgent(
            model_name=model_name,
            openai_api_key=openai_api_key,
            tools=tools,
            memory=memory
        )
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            cfg = RunnableConfig()
            cfg["callbacks"] = [st_cb]
            response = chat_agent.invoke_agent_executor(prompt, cfg)
            st.write(response["output"])
            st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]


login('.streamlit/config.yaml')
if st.session_state["authentication_status"]:
    create_chatbot()
