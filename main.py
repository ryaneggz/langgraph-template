## https://www.softgrade.org/sse-with-fastapi-react-langgraph/
from typing import Optional, List, Any, Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver

from src.flows.chat_agent import builder
from src.utils.visualize import visualize_graph
from src.utils.stream import event_stream
load_dotenv()

# Initialize graph and visualize once at start
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
visualize_graph(graph, "chat_agent")

app = FastAPI(
    title="Graph Agent Template 🤖",
    description="A template for building chatbots with LangGraph",
    contact={
        "name": "Ryan Eggleston",
        "email": "ryaneggleston@promptengineers.ai"
    },
    debug=True
)

class Parameters(BaseModel):
    query: str
    tools: Optional[List[Any]] = Field(default_factory=list)
    thread_id: int = Field(default=42)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the capital of France?",
                "tools": [],
                "thread_id": 42
            }
        }

@app.post("/llm")
def stream(body: Annotated[Parameters, Body()]):
    return StreamingResponse(
        event_stream(graph, body.query, body.tools, body.thread_id), 
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)