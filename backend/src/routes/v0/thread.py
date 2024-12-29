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
### List Checkpoints
################################################################################
@router.get(
    "/threads", 
    tags=[TAG],
    responses={
        status.HTTP_200_OK: {
            "description": "All existing threads.",
            "content": {
                "application/json": {
                    "example": Threads.model_json_schema()['examples']['threads']
                }
            }
        }
    }
)
def threads(
    username: str = Depends(verify_credentials),
    page: Optional[int] = Query(1, description="Page number", ge=1),
    per_page: Optional[int] = Query(10, description="Items per page", ge=1, le=100),
):
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        checkpointer = PostgresSaver(pool)
        checkpoints = checkpointer.list(
            config={},
            before=None,
            limit=None
        )
        # First collect all unique threads without the per_page limit
        seen_thread_ids = set()
        threads = []
        for checkpoint in checkpoints:
            thread_id = checkpoint.config['configurable']['thread_id']
            if thread_id not in seen_thread_ids:
                seen_thread_ids.add(thread_id)
                agent = Agent(thread_id, pool)
                checkpoint = agent.checkpoint()
                messages = checkpoint.get('channel_values', {}).get('messages')
                if isinstance(messages, list):
                    thread = Thread(
                        thread_id=thread_id,
                        checkpoint_ns='',
                        checkpoint_id=checkpoint.get('id'),
                        messages=messages,
                        ts=checkpoint.get('ts'),
                        v=checkpoint.get('v')
                    )
                    threads.append(thread.model_dump())
                    
        # Calculate pagination after collecting all threads
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_threads = threads[start_idx:end_idx]
        
        # Get the timestamp of the last thread for pagination
        last_ts = paginated_threads[-1]['ts'] if paginated_threads else None
        
        return JSONResponse(
            content={
                'threads': paginated_threads,
                'next_page': last_ts,
                'total': len(paginated_threads),
                'page': page,
                'per_page': per_page
            },
            status_code=status.HTTP_200_OK
        )

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
    before: Optional[str] = Query(None, description="List checkpoints created before this configuration."),
    limit: Optional[int] = Query(None, description="Maximum number of threads to return")
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
        
        items = []
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
                items.append(thread.model_dump())
                
        return JSONResponse(
            content={'checkpoints': items},
            status_code=status.HTTP_200_OK
        )