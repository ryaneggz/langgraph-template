## https://www.softgrade.org/sse-with-fastapi-react-langgraph/
import uuid
from typing import Annotated
from fastapi import FastAPI, Body, status, Request
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from psycopg_pool import ConnectionPool

from dotenv import load_dotenv

from src.constants import DB_URI, CONNECTION_POOL_KWARGS
from src.entities import Answer, LLMHTTPResponse, NewThread, ExistingThread
from src.utils.agent import Agent
load_dotenv()


app = FastAPI(
    title="LangGraph API Starter 🤖",
    summary=(
        "This is a simple API for building chatbots with LangGraph. " +
        "It allows you to create new threads, query existing threads, " +
        "and get the history of a thread."
    ),
    contact={
        "name": "Ryan Eggleston",
        "email": "ryaneggleston@promptengineers.ai"
    },
    debug=True
)

### Create New Thread
@app.post(
    "/llm", 
    tags=["LLM"], 
    responses={
        status.HTTP_200_OK: {
            "description": "Latest message from new thread.",
            "content": {
                "application/json": {
                    "example": Answer.Config.json_schema_extra['examples']['new_thread']
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
async def new_thread(
    request: Request,
    body: Annotated[NewThread, Body()]
):
    # Check if client accepts SSE
    if "text/event-stream" in request.headers.get("accept", ""):
        pool = ConnectionPool(
            conninfo=DB_URI,
            max_size=20,
            kwargs=CONNECTION_POOL_KWARGS,
        )
        agent = Agent(str(uuid.uuid4()), pool)
        agent.builder(tools=body.tools)
        messages = agent.messages(body.query, body.system)
        return agent.process(messages, "text/event-stream")

    # Default JSON response
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        agent = Agent(str(uuid.uuid4()), pool)
        agent.builder(tools=body.tools)
        messages = agent.messages(body.query, body.system)
        return agent.process(messages, "application/json")

## Query Existing Thread
@app.post(
    "/llm/{thread_id}", 
    tags=["LLM"],
    responses={
        status.HTTP_200_OK: {
            "description": "Latest message from existing thread.",
            "content": {
                "application/json": {
                    "example": Answer.Config.json_schema_extra['examples']['existing_thread']
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
async def existing_thread(
    request: Request,
    thread_id: str,
    body: Annotated[ExistingThread, Body()]
):
    if "text/event-stream" in request.headers.get("accept", ""):
        pool = ConnectionPool(
            conninfo=DB_URI,
            max_size=20,
            kwargs=CONNECTION_POOL_KWARGS,
        )
        agent = Agent(thread_id, pool)
        agent.builder(tools=body.tools)
        messages = [HumanMessage(content=body.query)]
        return agent.process(messages, "text/event-stream")

    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        agent = Agent(thread_id, pool)
        agent.builder(tools=body.tools)
        messages = [HumanMessage(content=body.query)]
        return agent.process(messages, "application/json")
    
### Query Thread History
@app.get(
    "/thread/{thread_id}", 
    tags=["Thread"],
    responses={
        status.HTTP_200_OK: {
            "description": "All messages from existing thread.",
            "content": {
                "application/json": {
                    "example": LLMHTTPResponse.Config.json_schema_extra['examples']['thread_history']
                }
            }
        }
    }
)
def thread_history(thread_id: str):
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


### Run Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")