# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ask, documents, scrape,download
import sys
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="Tender AI API",
    description="AI-powered tender assistant with RAG and search capabilities.",
    version="1.0.0"
)

# Enable CORS for all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(ask.router, prefix="")
app.include_router(documents.router, prefix="")
app.include_router(scrape.router, prefix="")
app.include_router(download.router, prefix="")

# Test route
@app.get("/start")
def start():
    return {"status": "✅ Tender AI is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
