# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     4_rag_sql_chatbot
   Description : 改进内容：
   1. 在没有输入数据库密码之前报错，应该是显示提示信息
   Author :       EveryFine
   Date：          2024/6/2
-------------------------------------------------
   Change Activity:
                   2024/6/2:
   Product:       PyCharm
-------------------------------------------------
"""
__author__ = 'EveryFine'

import os

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import SQLDatabase
from langchain_core.runnables import RunnableConfig

from home import login
from llm_clients.constants import tavily_tool, date_tool, current_time_tool
from llm_clients.openai_rag_sql_agent import OpenAIRagSqlAgent

st.set_page_config(page_title="RAG SQL Chatbot", page_icon="🐌")

login('.streamlit/config.yaml')


def create_chatbot():
    st.sidebar.header("🐌 RAG SQL Chatbot")
    st.markdown("# 🐌 RAG SQL Chatbot")
    st.markdown(
         """This **RAG SQL Chatbot** application leverages langchain technology to enable natural language 
         interactions with databases. Users simply input the database information to query and manage the database 
         using natural language. This approach simplifies database operations, making it accessible for non-technical 
         users to retrieve and manage data efficiently. """
    )

    model_name = "gpt-3.5-turbo"
    openai_api_key = os.getenv("OPENAI_API_KEY")
    uri = get_uri()
    db = SQLDatabase.from_uri(uri)
    if uri is None or uri == "":
        st.info("Please enter a database uri")
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
    if prompt := st.chat_input("Type your message here..."):
        st.chat_message("user").write(prompt)
        tools = [tavily_tool, date_tool, current_time_tool]

        rag_sql_agent = OpenAIRagSqlAgent(model_name=model_name,
                                          db=db,
                                          openai_api_key=openai_api_key,
                                          tools=tools,
                                          memory=memory)
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            cfg = RunnableConfig()
            cfg["callbacks"] = [st_cb]
            stream = rag_sql_agent.stream_agent_executor(prompt, cfg)
            response_container = st.empty()
            response_text = ""
            for chunk in stream:
                if output_chunk := chunk.get("output"):
                    response_text += output_chunk
                    # 实时更新Streamlit界面上的内容
                    response_container.markdown(response_text)
                if intermediate_steps := chunk.get("intermediate_steps"):
                    st.session_state.steps[str(len(msgs.messages) - 1)] = intermediate_steps

def get_uri():
    uri = ""
    with st.sidebar:
        db_type = st.selectbox(
            "Database Type",
            ("mysql", "sqlite"))
        if db_type == "mysql":
            mysql_host = st.text_input("Mysql Host", value="38.165.34.122")
            mysql_port = st.text_input("Mysql Port", value="3306")
            mysql_usename = st.text_input("Mysql Username", value="root")
            mysql_password = st.text_input("Mysql Password", type="password")
            mysql_database = st.text_input("Mysql Database", value="Chinook")
            uri = f"mysql+pymysql://{mysql_usename}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        elif db_type == "sqlite":
            sqlite_uri = st.text_input("Sqlite URI")
            uri = sqlite_uri
    return uri

if st.session_state["authentication_status"]:
    create_chatbot()
