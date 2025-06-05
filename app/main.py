from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from llm_scrapping import find_tenders

class PromptRequest(BaseModel):
    prompt: str

app = FastAPI()

@app.get("/start")
def start():
    return {"Start": "API is running!"}

@app.post("/get-tenders")
async def tender_scrapping(request: PromptRequest):
    return find_tenders(request.prompt) 




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)