

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("TEST APP RUNNING")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{path:path}")
async def options_handler(path: str):
    return {"ok": True}

@app.post("/signup")
async def signup(data: dict):
    return {
        "message": "success",
        "data": data
    }