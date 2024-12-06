import logging
import time
from typing import Dict, Optional
from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag.vectordb import QdrantDatabase

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
