from serpapi import GoogleSearch
SERP_API_KEY="caa4682cd14dbe8287235fa9a49e288c72f4476fd46cbf77db1fb6acbdfa16ee"
LOCATION = "India"
def search_results_serp(question):
    params = {
    "api_key": SERP_API_KEY,
    "engine": "google",
    "q": question,
    "location": LOCATION,
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results