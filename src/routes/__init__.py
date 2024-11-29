import uuid
from typing import Annotated

from fastapi import Body, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from loguru import logger
from psycopg_pool import ConnectionPool
from src.constants import DB_URI, CONNECTION_POOL_KWARGS

from src.entities import Answer, LLMHTTPResponse, NewThread, ExistingThread
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
        logger.info(f"Creating new thread with ID: {thread_id} and Tools: {body.tools} and Query: {body.query}")
        agent = Agent(thread_id, pool)
        agent.builder(tools=body.tools)
        messages = agent.messages(body.query, body.system)
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
        logger.info(f"Querying existing thread with ID: {thread_id} and Tools: {body.tools} and Query: {body.query}")
        agent.builder(tools=body.tools)
        messages = [HumanMessage(content=body.query)]
        return agent.process(messages, body.stream)
    
################################################################################
### Query Thread History
################################################################################
@router.get(
    "/thread/{thread_id}", 
    tags=[TAG],
    responses={
        status.HTTP_200_OK: {
            "description": "All messages from existing thread.",
            "content": {
                "application/json": {
                    "example": LLMHTTPResponse.model_json_schema()['examples']['thread_history']
                }
            }
        }
    }
)
def thread_history(
    thread_id: str,
    username: str = Depends(verify_credentials)
):
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        agent = Agent(thread_id, pool)
        checkpoint = agent.checkpoint()
        response = LLMHTTPResponse(
            thread_id=thread_id, 
            messages=checkpoint.get('channel_values').get('messages')
        )
        return JSONResponse(
            content=response.model_dump(),
            status_code=status.HTTP_200_OK
        )
        
################################################################################
### List Tools
################################################################################
from src.tools import tools
tool_names = [tool.name for tool in tools]
tools_response = {"tools": tool_names}
@router.get(
    "/tools", 
    tags=[TAG],
    responses={
        status.HTTP_200_OK: {
            "description": "All tools.",
            "content": {
                "application/json": {
                    "example": tools_response
                }
            }
        }
    }
)
def list_tools(username: str = Depends(verify_credentials)):
    return JSONResponse(
        content=tools_response,
        status_code=status.HTTP_200_OK
    )