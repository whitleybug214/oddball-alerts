from fastapi import FastAPI
from src.core.logging_config import configure_logging

configure_logging()

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}