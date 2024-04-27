# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     LlmOpenAI
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

from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from LlmClients.LlmClientBase import LlmClientBase


class OpenAIClient(LlmClientBase):

    def __init__(self, model_name, openai_api_key):
        super(OpenAIClient, self).__init__(model_name)
        self.openai_api_key = openai_api_key

    def get_stream_response(self, user_query, chat_history):
        template = """
        You are a helpful assistant. Answer the following questions considering the history of the conversation:

        Chat history: {chat_history}

        User question: {user_question}
        """

        prompt = ChatPromptTemplate.from_template(template)
        if not self.openai_api_key:
            raise ValueError("open api key is empty")
        if not self.model_name:
            self.model_name = "gpt-3.5-turbo"
        llm = ChatOpenAI(model=self.model_name, openai_api_key=self.openai_api_key)

        chain = prompt | llm | StrOutputParser()

        return chain.stream({
            "chat_history": chat_history,
            "user_question": user_query
        })
