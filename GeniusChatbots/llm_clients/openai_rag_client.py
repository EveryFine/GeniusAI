# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     openai_rag_client
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

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from llm_clients.llm_client_base import LlmClientBase


class OpenAIRagClient(LlmClientBase):
    def __init__(self, model_name, openai_api_key):
        super(OpenAIRagClient, self).__init__(model_name)
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, streaming=True)

    def get_invoke_response(self, user_input, chat_history, vector_store):
        retriever_chain = self.get_context_retriever_chain(vector_store)
        conversation_rag_chain = self.get_conversational_rag_chain(retriever_chain)

        response = conversation_rag_chain.invoke({
            "chat_history": chat_history,
            "input": user_input
        })

        return response['answer']

    def get_context_retriever_chain(self, vector_store):
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

    def get_conversational_rag_chain(self, retriever_chain):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the user's questions based on the below context:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])
        stuff_documents_chain = create_stuff_documents_chain(self.llm, prompt)

        return create_retrieval_chain(retriever_chain, stuff_documents_chain)
