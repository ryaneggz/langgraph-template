import uuid
from typing import Annotated

from fastapi import Body, status, Depends, APIRouter, Request
from loguru import logger
from psycopg_pool import ConnectionPool
from src.constants import DB_URI, CONNECTION_POOL_KWARGS

from src.entities import Answer, NewThread, ExistingThread
from src.utils.agent import Agent
from src.utils.auth import verify_credentials

TAG = "Agent"
router = APIRouter(tags=[TAG])

################################################################################
### Create New Thread
################################################################################
@router.post(
    "/llm", 
    responses={
        status.HTTP_200_OK: {
            "description": "Latest message from new thread.",
            "content": {
                "application/json": {
                    "example": Answer.model_json_schema()['examples']['new_thread']
                },
                "text/event-stream": {
                    "description": "Server-sent events stream",
                    "schema": {
                        "type": "string",
                        "format": "binary",
                        "example": 'data: {"thread_id": "e208fbc9-92cd-4f50-9286-6eab533693c4", "event": "ai_chunk", "content": [{"text": "Hello", "type": "text", "index": 0}]}\n\n'
                    }
                }
            }
        }
    }
)
def new_thread(
    request: Request,
    body: Annotated[NewThread, Body()],
    username: str = Depends(verify_credentials)
):
    thread_id = str(uuid.uuid4())
    tools_str = f"and Tools: {', '.join(body.tools)}" if body.tools else ""
    logger.info(f"Creating new thread with ID: {thread_id} {tools_str} and Query: {body.query}")
    
    if "text/event-stream" in request.headers.get("accept", ""):
        pool = ConnectionPool(
            conninfo=DB_URI,
            max_size=20,
            kwargs=CONNECTION_POOL_KWARGS,
        )
        agent = Agent(thread_id, pool)
        agent.builder(tools=body.tools, model_name=body.model)
        messages = agent.messages(body.query, body.system, body.images)
        return agent.process(messages, "text/event-stream")
    
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        agent = Agent(thread_id, pool)
        agent.builder(tools=body.tools, model_name=body.model)
        messages = agent.messages(body.query, body.system, body.images)
        return agent.process(messages, "application/json")
    
################################################################################
### Query Existing Thread
################################################################################
@router.post(
    "/llm/{thread_id}", 
    tags=[TAG],
    responses={
        status.HTTP_200_OK: {
            "description": "Latest message from existing thread.",
            "content": {
                "application/json": {
                    "example": Answer.model_json_schema()['examples']['existing_thread']
                },
                "text/event-stream": {
                    "description": "Server-sent events stream",
                    "schema": {
                        "type": "string",
                        "format": "binary",
                        "example": 'data: {"thread_id": "e208fbc9-92cd-4f50-9286-6eab533693c4", "event": "ai_chunk", "content": [{"text": "Hello", "type": "text", "index": 0}]}\n\n'
                    }
                }
            }
        }
    }
)
def existing_thread(
    request: Request,
    thread_id: str, 
    body: Annotated[ExistingThread, Body()],
    username: str = Depends(verify_credentials)
):
    tools_str = f"and Tools: {', '.join(body.tools)}" if body.tools else ""
    logger.info(f"Querying existing thread with ID: {thread_id} {tools_str} and Query: {body.query}")
    
    if "text/event-stream" in request.headers.get("accept", ""):
        pool = ConnectionPool(
            conninfo=DB_URI,
            max_size=20,
            kwargs=CONNECTION_POOL_KWARGS,
        )
        agent = Agent(thread_id, pool)
        agent.builder(tools=body.tools, model_name=body.model)
        messages = agent.messages(query=body.query, images=body.images)
        return agent.process(messages, "text/event-stream")
    
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:  
        agent = Agent(thread_id, pool)
        agent.builder(tools=body.tools, model_name=body.model)
        messages = agent.messages(query=body.query, images=body.images)
        return agent.process(messages, "application/json")