import logging
from fastapi import FastAPI, HTTPException

# import time
# from typing import Dict, Optional
# from celery.result import AsyncResult
# from pydantic import BaseModel
# from src.rag.vectordb import QdrantClient

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

