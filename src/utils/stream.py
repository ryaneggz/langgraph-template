from typing import Optional, List, Any, Annotated

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
from pydantic import BaseModel


from langchain_core.messages import HumanMessage, ToolMessage, AnyMessage
from src.utils.system import read_system_message, SystemPaths

class Configurable(BaseModel):
    thread_id: str

class StreamInput(BaseModel):
    messages: list
    configurable: Configurable
    
class LLMHTTPResponse(BaseModel):
    # system: Optional[str] = Field(default="You are a helpful assistant.")
    messages: list[AnyMessage] = Field(default_factory=list)
    # tools: Optional[List[Any]] = Field(default_factory=list)
    # thread_id: str = Field(default="42")
    
class Parameters(BaseModel):
    query: str
    tools: Optional[List[Any]] = Field(default_factory=list)
    thread_id: str = Field(default="42")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the capital of France?",
                "tools": [],
                "thread_id": "42"
            }
        }


def stream_graph_updates(graph: StateGraph, input: StreamInput):
    for event in graph.stream(input, input['configurable'], stream_mode='values'):
        if event.get('call_chat_model'):
            print("Bot: " + event['call_chat_model']['messages'][-1].content)
        elif event.get('error'):
            print("Error: " + event['error']['messages'][-1].content)
        elif event.get('messages'):
            print("Bot: " + event['messages'][-1].content)
        else:
            print("Unknown event: " + str(event))
            
def stream_graph_tokens(
    graph: StateGraph, 
    input: str, 
    config: Configurable, 
    stream_mode: str = "messages"
):
    print("<< Bot: ", end="", flush=True)
    for msg, metadata in graph.stream(
        {"messages": input}, config, stream_mode=stream_mode
    ):
        if msg.content and not isinstance(msg, HumanMessage):
            print(msg.content, end="", flush=True)
            
            
def stream_graph_values(
    graph: StateGraph, 
    input: str, 
    config,
    stream_mode: str = "values"
):
    for chunk in graph.stream(
        input, 
        {"configurable": config},
        stream_mode=stream_mode
    ):
        chunk["messages"][-1].pretty_print()
        
def event_stream(
    graph: StateGraph, 
    query: str,
    tools: list[BaseTool] = [], 
    thread_id: str = None
):
    initial_state = {
        "system": read_system_message(SystemPaths.COT_MCTS.value),
        "messages": [HumanMessage(content=query)],
        "tools": tools,
        "thread_id": thread_id
    }

    for chunk in graph.stream(initial_state, {'configurable': {'thread_id': thread_id}}):
        for node_name, node_results in chunk.items():
            chunk_messages = node_results.get("messages", [])
            for message in chunk_messages:
                if not message.content:
                    continue
                if isinstance(message, ToolMessage):
                    event_str = "event: tool_event"
                else:
                    event_str = "event: ai_event"
                data_str = f"data: {message.content}"
                yield f"{event_str}\n{data_str}\n\n"
                
      

## https://github.com/langchain-ai/langgraph/tree/main/libs/checkpoint-postgres
## https://langchain-ai.github.io/langgraph/how-tos/persistence_postgres/#with-a-connection-pool 
## https://api.python.langchain.com/en/latest/checkpoint/langchain_postgres.checkpoint.PostgresSaver.html         
def http_response(
    graph: StateGraph, 
    query: str,
    tools: list[BaseTool] = [], 
    thread_id: str = None,
    checkpointer: any = None
):
    initial_state = {
        "system": read_system_message(SystemPaths.COT_MCTS.value),
        "messages": [HumanMessage(content=query)],
        "tools": tools,
        "thread_id": thread_id
    }
    config = {'configurable': {'thread_id': thread_id}}
    res = graph.invoke(initial_state, config)
    # checkpoint = checkpointer.get(config)
    # updated = checkpointer.put(
    #     {"configurable": {"thread_id": thread_id, "checkpoint_ns": "chat_agent"}}, 
    #     checkpoint,
    #     {}, 
    #     {}
    # )
    # print(updated)
    return LLMHTTPResponse(**res)   