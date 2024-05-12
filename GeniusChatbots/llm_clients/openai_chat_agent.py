# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     openai_chat_agent
   Description :
   Author :       EveryFine
   Date：          2024/5/12
-------------------------------------------------
   Change Activity:
                   2024/5/12:
   Product:       PyCharm
-------------------------------------------------
"""
__author__ = 'EveryFine'

from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain_community.chat_models import ChatOpenAI

from llm_clients.llm_client_base import LlmClientBase


class OpenAIChatAgent(LlmClientBase):

    def __init__(self, model_name, openai_api_key, tools, memory):
        super(OpenAIChatAgent, self).__init__(model_name)
        self.openai_api_key = openai_api_key
        self.tools = tools
        self.llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, streaming=True)
        self.chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=self.llm, tools=tools)
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.chat_agent,
            tools=self.tools,
            memory=memory,
            return_intermediate_steps=True,
            handle_parsing_errors=True
        )

    def invoke_agent_executor(self, prompt, cfg):
        response = self.agent_executor.invoke(prompt, cfg)
        return response
