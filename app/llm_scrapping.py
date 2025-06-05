from tavily import TavilyClient
client = TavilyClient("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")

def find_tenders(prompt: str):
    """
    Function to find tenders using Tavily API.
    """
    response = client.search(
        query=f"{prompt}",
        search_depth="advanced",
        max_results=20,

    )
    return response