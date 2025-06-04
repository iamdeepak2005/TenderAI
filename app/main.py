from fastapi import FastAPI

app = FastAPI(title="Tender AI", version="1.0")

@app.get("/start")
def start():
    return {"Start": "AI Tendering Process"}
