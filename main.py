## https://www.softgrade.org/sse-with-fastapi-react-langgraph/
import uuid
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from psycopg_pool import ConnectionPool

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
                }
            }
        }
    }
)
def new_thread(body: Annotated[NewThread, Body()]):
    if not body.stream:
        # Non-streaming response can use context manager
        with ConnectionPool(
            conninfo=DB_URI,
            max_size=20,
            kwargs=CONNECTION_POOL_KWARGS,
        ) as pool:
            agent = Agent(str(uuid.uuid4()), pool)
            agent.builder(tools=body.tools)
            messages = agent.messages(body.query, body.system)
            return agent.process(messages, body.stream)
    
    # For streaming, create pool without context manager
    pool = ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    )
    agent = Agent(str(uuid.uuid4()), pool)
    agent.builder(tools=body.tools)
    messages = agent.messages(body.query, body.system)
    return agent.process(messages, body.stream)

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
                }
            }
        }
    }
)
def existing_thread(
    thread_id: str, 
    body: Annotated[ExistingThread, Body()]
):
    if not body.stream:
        # Non-streaming response can use context manager
        with ConnectionPool(
            conninfo=DB_URI,
            max_size=20,
            kwargs=CONNECTION_POOL_KWARGS,
        ) as pool:  
            agent = Agent(thread_id, pool)
            agent.builder(tools=body.tools)
            messages = [HumanMessage(content=body.query)]
            return agent.process(messages, body.stream)
    
    # For streaming, create pool without context manager
    pool = ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    )
    agent = Agent(thread_id, pool)
    agent.builder(tools=body.tools)
    messages = [HumanMessage(content=body.query)]
    return agent.process(messages, body.stream)
    
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
    uvicorn.run(app, host="0.0.0.0", port=8000)