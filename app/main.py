from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from llm_scrapping import find_tenders
from scraping_by_url import scrape
from serpapi_utils import search_results_serp
class PromptRequest(BaseModel):
    prompt: str

class URLRequest(BaseModel):
    url: str

app = FastAPI()
GOOGLE_PROGRAMMABLE_SEARCH="AIzaSyBMvFZgCGXQ7twey38F9sBGkEJQ2nPFCO8"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/start")
def start():
    return {"Start": "API is running!"}

@app.post("/get-tenders")
async def tender_scrapping(request: PromptRequest):
    return find_tenders(request.prompt) 

@app.post("/scrape-url")
async def url_srcap(request: URLRequest):
    return scrape(request.url)

@app.post("/scrape-google")
async def google_scrap(prompt: PromptRequest):
    return search_results_serp(prompt.prompt)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)