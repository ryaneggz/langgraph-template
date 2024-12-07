import uuid
from typing import Annotated

from fastapi import Body, status, Depends, APIRouter
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
                }
            }
        }
    }
)
def new_thread(
    body: Annotated[NewThread, Body()],
    username: str = Depends(verify_credentials)
):
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        thread_id = str(uuid.uuid4())
        tools_str = f"and Tools: {', '.join(body.tools)}" if body.tools else ""
        logger.info(f"Creating new thread with ID: {thread_id} {tools_str} and Query: {body.query}")
        agent = Agent(thread_id, pool)
        agent.builder(tools=body.tools)
        messages = agent.messages(body.query, body.system, body.images)
        return agent.process(messages, body.stream)
    
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
                }
            }
        }
    }
)
def existing_thread(
    thread_id: str, 
    body: Annotated[ExistingThread, Body()],
    username: str = Depends(verify_credentials)
):
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:  
        agent = Agent(thread_id, pool)
        tools_str = f"and Tools: {', '.join(body.tools)}" if body.tools else ""
        logger.info(f"Querying existing thread with ID: {thread_id} {tools_str} and Query: {body.query}")
        agent.builder(tools=body.tools)
        messages = agent.messages(query=body.query, images=body.images)
        return agent.process(messages, body.stream)