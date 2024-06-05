# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     openai_rag_sql_agent
   Description :
   Author :       EveryFine
   Date：          2024/6/2
-------------------------------------------------
   Change Activity:
                   2024/6/2:
   Product:       PyCharm
-------------------------------------------------
"""
__author__ = 'EveryFine'

from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_openai import ChatOpenAI

from llm_clients.llm_client_base import LlmClientBase
from llm_clients.sql_agent_constants import CUSTOM_SUFFIX


class OpenAIRagSqlAgent(LlmClientBase):
    def __init__(self, model_name, db, openai_api_key, tools, memory):
        super(OpenAIRagSqlAgent, self).__init__(model_name)
        self.openai_api_key = openai_api_key
        self.tools = tools
        self.db = db
        self.llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, streaming=True)
        self.toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0))
        # self.agent_executor = create_sql_agent(llm=self.llm,
        #                                        db=self.db,
        #                                        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #                                        # agent_type="openai-tools",
        #                                        input_variables=["input", "agent_scratchpad", "history"],
        #                                        suffix=CUSTOM_SUFFIX,
        #                                        extra_tools=tools,
        #                                        verbose=True,
        #                                        agent_executor_kwargs={
        #                                            "memory": memory,
        #                                            "return_intermediate_steps": True,
        #                                            "handle_parsing_errors": True
        #                                        },
        #                                        )
        all_tools = tools + self.toolkit.get_tools()
        self.agent_executor = initialize_agent(all_tools,
                                               self.llm,
                                               # agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                               agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                               verbose=True,
                                               memory=memory,
                                               return_intermediate_steps=True,
                                               handle_parsing_errors=True)

    def invoke_agent_executor(self, prompt, cfg):
        response = self.agent_executor.invoke(prompt, cfg)
        return response

    def stream_agent_executor(self, prompt, cfg):
        response = self.agent_executor.stream(prompt, cfg)
        return response
