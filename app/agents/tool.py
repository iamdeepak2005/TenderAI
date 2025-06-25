# app/agents/tools.py

from langchain_core.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
from ..config import SERP_API_KEY

# Initialize SerpAPI wrapper
search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)

# Define tool for web search
web_search_tool = Tool(
    name="Web Search",
    func=search.run,
    description="Useful for fetching real-time news, job listings, or any web content."
)