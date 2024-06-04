# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     constants
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

from datetime import datetime

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool


def get_today_date(query: str) -> str:
    """
    Useful to get the date of today.
    """
    # Getting today's date in string format
    today_date_string = datetime.now().strftime("%Y-%m-%d")
    return today_date_string


def get_current_time(query: str) -> str:
    """
    Useful to get the current datetime of now.
    """
    # Getting today's date in string format
    current_time = datetime.now().isoformat()
    return current_time


date_tool = Tool.from_function(
    name="get_today_date",
    func=get_today_date,
    description="Useful to get the date of today.",
)
current_time_tool = Tool.from_function(
    name="get_current_time",
    func=get_current_time,
    description="Useful to get the time of current.",
)

tavily_tool = TavilySearchResults()
