# app/agents/agent_initializer.py

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from .tool import web_search_tool
from ..config import OPENROUTER_API_KEY
from .tools import clause_tool, summary_tool, section_list_tool


def get_llm():
    return ChatOpenAI(
        model="deepseek/deepseek-r1:free",
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7
    )


def get_agent():
    llm = get_llm()
    tools = [web_search_tool]
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )


def get_agent_rag():
    llm = get_llm()
    tools = [clause_tool, summary_tool, section_list_tool]
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )