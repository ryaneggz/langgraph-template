from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

class Configurable(BaseModel):
    enabled: bool
    session_id: str

class StreamInput(BaseModel):
    messages: list
    configurable: Configurable


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