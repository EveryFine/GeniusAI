# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     3_rag_website_chatbot
   Description :
   Author :       EveryFine
   Date：          2024/5/19
-------------------------------------------------
   Change Activity:
                   2024/5/19:
   Product:       PyCharm
-------------------------------------------------
"""
__author__ = 'EveryFine'

import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from home import login
import streamlit as st

'''
REFERENCE
https://github.com/alejandro-ao/chat-with-websites/blob/master/src/app.py
改进项：
1. 流式输出结果stream
2. 将模型相关内容放入单独的类中
3. 在更改url时弹出是否更新url的提示，用户确认之后增加新网站的内容到向量库中
4. 使用langsmith跟踪所发出的请求结果
5. 最好运行过程中能够显示所引用的内容源
'''




def get_vectorstore_from_url(url):
    # get the text in document form
    loader = WebBaseLoader(url)
    document = loader.load()

    # split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)

    # create a vectorstore from the chunks
    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())

    return vector_store


def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user",
         "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    return retriever_chain


def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)


def create_chatbot():
    st.sidebar.header("🦀 RAG Website Chatbot")
    st.markdown("# 🦀 RAG Website Chatbot")
    st.markdown(
        """
        The **AG Website Chatbot** leverages langchain's RAG technology to enable dynamic conversations about website content. Users simply input a URL and the chatbot provides immediate, context-aware insights, facilitating a deeper understanding of web content. 
        """
    )
    model_name = "gpt-3.5-turbo"
    openai_api_key = os.getenv("OPENAI_API_KEY")
    with st.sidebar:
        website_url = st.text_input("Website URL")
    if website_url is None or website_url == "":
        st.info("Please enter a website URL")
    else:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Hello, I am a bot. How can I help you?"),
            ]
        if "vector_store" not in st.session_state:
            st.session_state.vector_store = get_vectorstore_from_url(website_url)
        user_query = st.chat_input("Type your message here...")
        if user_query is not None and user_query != "":
            response = get_response(user_query)
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=response))
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)

def get_response(user_input):
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })

    return response['answer']

login('.streamlit/config.yaml')
if st.session_state["authentication_status"]:
    create_chatbot()
