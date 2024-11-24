## https://www.softgrade.org/sse-with-fastapi-react-langgraph/
from typing import Annotated
import json

from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from src.infra.db import get_db_checkpointer
from src.flows.chat_agent import builder
from src.utils.visualize import visualize_graph
from src.utils.stream import http_response, Parameters
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

@app.post("/llm")
def llm_query(body: Annotated[Parameters, Body()]):
    # Create a global connection pool
    checkpointer = get_db_checkpointer()
    graph = builder.compile(checkpointer=checkpointer)
    visualize_graph(graph, "chat_agent")
    
    state = http_response(
        graph, 
        body.query, 
        body.tools, 
        body.thread_id,
        checkpointer
    )
    
    return JSONResponse(
        content=state.model_dump(),
        status_code=200
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)