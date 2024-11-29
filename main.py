## https://www.softgrade.org/sse-with-fastapi-react-langgraph/
import os
import uuid
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from loguru import logger
from psycopg_pool import ConnectionPool

from src.constants import DB_URI, CONNECTION_POOL_KWARGS
from src.entities import Answer, LLMHTTPResponse, NewThread, ExistingThread
from src.utils.agent import Agent
load_dotenv()


app = FastAPI(
    title="LangGraph API Starter 🤖", 
    description=(
        "This is a simple API for building chatbots with LangGraph. " +
        "It allows you to create new threads, query existing threads, " +
        "and get the history of a thread.\n Check out the repo on " +
        f"<a href='https://github.com/ryaneggz/langgraph-template'>Github</a>"
    ),
    contact={
        "name": "Ryan Eggleston",
        "email": "ryaneggleston@promptengineers.ai"
    },
    debug=True,
    docs_url="/"
)

TAG = "Agent"

### Create New Thread
@app.post(
    "/llm", 
    tags=[TAG], 
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
def new_thread(body: Annotated[NewThread, Body()]):
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

## Query Existing Thread
@app.post(
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
    body: Annotated[ExistingThread, Body()]
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
    
### Query Thread History
@app.get(
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

### List Tools
from src.tools import tools
tool_names = [tool.name for tool in tools]
tools_response = {"tools": tool_names}
@app.get(
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
def list_tools():
    return JSONResponse(
        content=tools_response,
        status_code=status.HTTP_200_OK
    )

### Run Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=str(os.getenv("HOST", "0.0.0.0")), 
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("LOG_LEVEL", "info")
    )