# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sql_agent_constants
   Description :
   Author :       EveryFine
   Date：          2024/6/4
-------------------------------------------------
   Change Activity:
                   2024/6/4:
   Product:       PyCharm
-------------------------------------------------
"""
__author__ = 'EveryFine'

CUSTOM_SUFFIX = """Begin!

Relevant pieces of previous conversation:
{history}
(Note: Only reference this information if it is relevant to the current query.)

Question: {input}
Thought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables. 
My final response must be delivered in the language of the user's query.

{agent_scratchpad}
"""