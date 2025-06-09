from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from llm_scrapping import find_tenders
from scraping_by_url import scrape
from serpapi_utils import search_results_serp
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
from rag_utils import *
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import asyncio
class PromptRequest(BaseModel):
    prompt: str

class URLRequest(BaseModel):
    url: str

app = FastAPI()
GOOGLE_PROGRAMMABLE_SEARCH="AIzaSyBMvFZgCGXQ7twey38F9sBGkEJQ2nPFCO8"
UPLOAD_DIR = "docs/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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



@app.post("/upload/")
async def upload_docs(files: list[UploadFile]):
    # Clear vector store
    shutil.rmtree("backend/vector_store", ignore_errors=True)
    os.makedirs("backend/vector_store", exist_ok=True)

    paths = []
    for file in files:
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        paths.append(path)

    process_documents(paths)
    return {"message": "Documents processed"}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    def generate():
        for section_response in ask_detail(question):
            yield section_response
    return StreamingResponse(generate(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


