# https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.postgres.BasePostgresSaver

from fastapi import status, Depends, APIRouter, Query
from fastapi.responses import JSONResponse
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from typing import Optional

from src.constants import DB_URI, CONNECTION_POOL_KWARGS
from src.entities import Thread, Threads
from src.utils.agent import Agent
from src.utils.auth import verify_credentials

TAG = "Agent"
router = APIRouter(tags=[TAG])


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
                    "example": Thread.model_json_schema()['examples']['thread_history']
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
        response = Thread(
            thread_id=thread_id, 
            messages=checkpoint.get('channel_values').get('messages')
        )
        return JSONResponse(
            content=response.model_dump(),
            status_code=status.HTTP_200_OK
        )
        
################################################################################
### List Checkpoints
################################################################################
@router.get(
    "/checkpoints", 
    tags=[TAG],
    responses={
        status.HTTP_200_OK: {
            "description": "All existing checkpoints.",
            "content": {
                "application/json": {
                    "example": Threads.model_json_schema()['examples']['threads']
                }
            }
        }
    }
)
def checkpoints(
    username: str = Depends(verify_credentials),
    thread_id: Optional[str] = Query(None, description="Filter by thread ID"),
    checkpoint_id: Optional[str] = Query(None, description="Filter by checkpoint ID"),
    before: Optional[str] = Query(None, description="List threads before this thread ID"),
    limit: Optional[int] = Query(25, description="Maximum number of threads to return")
):
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        checkpointer = PostgresSaver(pool)
        
        # Build the base config and filter
        config = {}
        if thread_id:
            config = {"configurable": {"thread_id": thread_id}}
        elif checkpoint_id:
            config = {"configurable": {"checkpoint_id": checkpoint_id}}
            
        # Build the before config if provided
        before_config = {"configurable": {"thread_id": before}} if before else None
        
        checkpoints = checkpointer.list(
            config=config,
            before=before_config,
            limit=limit
        )
        
        threads = []
        for checkpoint in checkpoints:
            config = checkpoint.config['configurable']
            checkpoint = checkpoint.checkpoint
            messages = checkpoint.get('channel_values', {}).get('messages')
            if isinstance(messages, list):
                thread = Thread(
                    thread_id=config.get('thread_id'),
                    checkpoint_ns=config.get('checkpoint_ns'),
                    checkpoint_id=config.get('checkpoint_id'),
                    messages=messages,
                    ts=checkpoint.get('ts'),
                    v=checkpoint.get('v')
                )
                threads.append(thread.model_dump())
                
        return JSONResponse(
            content={'checkpoints': threads},
            status_code=status.HTTP_200_OK
        )