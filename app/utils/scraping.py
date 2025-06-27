from serpapi import GoogleSearch
from ..config import SERP_API_KEY

def search_results_serp(query: str, max_results: int = 1000):
    all_organic_results = []
    params = {
        "q": f"{query} site:bidplus.gem.gov.in",
        "api_key": SERP_API_KEY,
        "num": 100,
        "start": 0
    }

    while True:
        search = GoogleSearch(params)
        results = search.get_dict()

        organic_results = results.get("organic_results", [])
        if not organic_results:
            break  # Stop if no more results

        all_organic_results.extend(organic_results)

        # Check if we hit the max desired results
        if len(all_organic_results) >= max_results:
            break

        # Use SerpApi pagination link if available
        next_page_link = results.get("serpapi_pagination", {}).get("next")
        if next_page_link:
            # Update params by extracting start value from the next_page_link
            # Example link: https://serpapi.com/search.json?...&start=100
            from urllib.parse import urlparse, parse_qs

            parsed_url = urlparse(next_page_link)
            query_params = parse_qs(parsed_url.query)
            params["start"] = int(query_params.get("start", [0])[0])
        else:
            break  # No next page available

    # Process and format the results
    parsed_results = []
    for result in all_organic_results[:max_results]:
        parsed_results.append({
            "title": result.get("title", "No Title"),
            "description": result.get("snippet", "No Description"),
            "link": result.get("link", "No Link"),
            # "position": result.get("position", None),
            # "displayed_link": result.get("displayed_link", ""),
            # "source": result.get("source", ""),
        })

    return {
        "results": parsed_results,
        "count": len(parsed_results)
    }
