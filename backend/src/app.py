import logging
from fastapi import FastAPI, HTTPException

import time
from typing import Dict, Optional
from celery.result import AsyncResult
from pydantic import BaseModel
from src.rag.vectordb import qdrant_client
from task.llm import llm_handle_message

logger = logging.getLogger(__name__)

app = FastAPI()

class CompleteRequest(BaseModel):
    bot_id: Optional[str] = 'bot home loan'
    user_id: str
    user_message: str
    sync_request: Optional[bool] = False
 

@app.get("/")
async def root():
    return {"Welcome to Intelligent home loan processing"}


@app.post("/chat/complete")
async def complete(data:CompleteRequest):
    bot_id  = data.bot_id
    user_id = data.user_id
    user_message = data.user_message
    logger.info(f"Complete chat from user {user_id} to {bot_id}: {user_message}")

    if not user_message or not user_id:
        raise HTTPException(status_code=400, detail="User id and user message are required")

    if data.sync_request:
        response = llm_handle_message(bot_id, user_id, user_message)
        return {"response": response}
    else:
        task = "123"
        return {"task_id": task}

@app.post("/collection/create")
async def create_vector_collection(data: Dict):
    collection_name = data.get("collection_data")
    create_status = qdrant_client.create_collection(collection_name)
    logging.info(f"Create collection {collection_name} status: {create_status}")
    return {"status": create_status is not None}