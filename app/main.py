from fastapi import FastAPI

app = FastAPI()

@app.get("/start")
def start():
    return {"Start": "API is running!"}
