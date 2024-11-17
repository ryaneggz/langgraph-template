from langgraph.graph import StateGraph, END, START

from src.utils.visualize import visualize_graph
from src.utils.state import State
from src.utils.nodes import call_model, should_run

builder = StateGraph(State)

# Nodes
builder.add_node("call_model", call_model)

# Add conditional edge
builder.add_conditional_edges(START, should_run)
# Connect nodes to the end
builder.add_edge("call_model", END)
graph = builder.compile()
# graph.debug = True
visualize_graph(graph, "should_run_end")