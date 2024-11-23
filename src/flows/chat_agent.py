import os
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, add_messages, START, END
from langchain_core.messages import AnyMessage, SystemMessage

from src.utils.llm import LLMWrapper, ModelName
from src.utils.tools import tool_node

class State(TypedDict):
    system: str
    messages: Annotated[list[AnyMessage], add_messages]
    tools: list
    thread_id: int


def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "actions"
    return END


def call_model(state: State):
    messages = state["messages"]
    # Get tools from state that match available tool names
    selected_tools = []
    if "tools" in state:
        from src.utils.tools import tools
        selected_tools = [tool for tool in tools if tool.name in state["tools"]]
    
    llm = LLMWrapper(
        model_name=ModelName.ANTHROPIC,
        api_key=os.getenv("ANTHROPIC_API_KEY"), 
        tools=selected_tools
    )
    if not isinstance(messages[0], SystemMessage):
        messages.insert(0, SystemMessage(content=state.get("system", "You are a helpful assistant.")))
    response = llm.invoke(messages)
    return {"messages": [response]}


builder = StateGraph(State)

# Define the two nodes we will cycle between
builder.add_node("agent", call_model)
builder.add_node("actions", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue, ["actions", END])
builder.add_edge("actions", "agent")