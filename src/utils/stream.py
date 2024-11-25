from langgraph.graph import StateGraph
from langchain_core.messages import AnyMessage, ToolMessage

async def event_stream(
    graph: StateGraph, 
    messages: list[AnyMessage],
    thread_id: str = None
):
    for chunk in graph.stream(
        {"messages": messages}, 
        {'configurable': {'thread_id': thread_id}}
    ):
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
                print(f"{event_str}\n{data_str}\n\n")
                yield f"{event_str}\n{data_str}\n\n"
                
                
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