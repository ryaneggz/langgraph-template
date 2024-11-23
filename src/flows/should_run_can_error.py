from langgraph.graph import StateGraph, END, START

from utils.visualize import visualize_graph
from utils.state import State
from utils.nodes import call_chat_model, should_run, error_node

builder = StateGraph(State)

# Nodes
builder.add_node("call_chat_model", call_chat_model)
builder.add_node("error", error_node)

# Add conditional edge
builder.add_conditional_edges(START, should_run)
# Connect nodes to the end
builder.add_edge("call_chat_model", END)
builder.add_edge("error", END)
graph = builder.compile()
# graph.debug = True
visualize_graph(graph, "should_run_can_error")