from langgraph.graph import StateGraph
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
from pydantic import BaseModel


from langchain_core.messages import HumanMessage, ToolMessage
from src.utils.system import read_system_message, SystemPaths

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
        
def event_stream(
    graph: StateGraph, 
    query: str,
    tools: list[BaseTool] = [], 
    thread_id: int = 42
):
    initial_state = {
        "system": read_system_message(SystemPaths.COT_MCTS.value),
        "messages": [HumanMessage(content=query)],
        "tools": tools,
        "thread_id": {"enabled": True, "session_id": thread_id}
    }
    for chunk in graph.stream(initial_state, {"thread_id": thread_id}):
        for node_name, node_results in chunk.items():
            chunk_messages = node_results.get("messages", [])
            for message in chunk_messages:
                # You can have any logic you like here
                # The important part is the yield
                if not message.content:
                    continue
                if isinstance(message, ToolMessage):
                    event_str = "event: tool_event"
                else:
                    event_str = "event: ai_event"
                data_str = f"data: {message.content}"
                yield f"{event_str}\n{data_str}\n\n"