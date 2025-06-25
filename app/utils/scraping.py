from serpapi import GoogleSearch
from ..config import SERP_API_KEY
def search_results_serp(query: str, num_results: int = 10):
    params = {
        "q": f"{query} site:bidplus.gem.gov.in",
        "api_key": SERP_API_KEY,
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])

    parsed_results = []
    for result in organic_results:
        parsed_results.append({
            "title": result.get("title", "No Title"),
            "description": result.get("snippet", "No Description"),
            "link": result.get("link", "No Link")
        })

    return {"results": parsed_results}
