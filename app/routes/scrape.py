# app/routes/scrape.py

from fastapi import APIRouter
from pydantic import BaseModel
from ..utils.scraping import search_results_serp  # You can define these in utils

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

class URLRequest(BaseModel):
    url: str

# @router.post("/scrape-url/")
# async def scrape_url(request: URLRequest):
#     return scrape_from_url(request.url)

@router.post("/scrape-google/")
async def google_search(request: PromptRequest):
    return search_results_serp(request.prompt)
