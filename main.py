## https://www.softgrade.org/sse-with-fastapi-react-langgraph/
import uuid
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse

from src.entities import LLMHTTPResponse, LLMQuery
from src.utils.agent import Agent
load_dotenv()

app = FastAPI(
    title="Graph Agent Template 🤖",
    description="A template for building chatbots with LangGraph",
    contact={
        "name": "Ryan Eggleston",
        "email": "ryaneggleston@promptengineers.ai"
    },
    debug=True
)

### Create New Thread
@app.post("/llm")
def llm_query_new_thread(body: Annotated[LLMQuery, Body()]):
    agent = Agent(str(uuid.uuid4()))
    agent.builder(tools=body.tools)
    messages = agent.messages(body.query, body.system)
    return agent.process(messages, body.stream)

### Query Existing Thread
@app.post("/llm/{thread_id}")
def llm_query_existing_thread(thread_id: str, body: Annotated[LLMQuery, Body()]):
    agent = Agent(thread_id)
    agent.builder(tools=body.tools)
    messages = agent.messages(body.query, body.system)
    return agent.process(messages, body.stream)
    
### Query Agent History
@app.get("/llm/thread/{thread_id}")
def llm_history(thread_id: str):
    agent = Agent(thread_id)
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