
import traceback

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

from src.flows.chat_agent import builder
from src.utils.stream import stream_graph_values
from src.utils.system import read_system_message, SystemPaths
from src.utils.visualize import visualize_graph
load_dotenv()

# Initialize graph and visualize once at start
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
visualize_graph(graph, "chat_agent")

# Chat loop
while True:
    try:
        user_input = input("\n>> User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_values(
            graph,
            {
                "system": read_system_message(SystemPaths.COT_MCTS.value), 
                "messages": [
                    ('human', user_input)
                ], 
                "tools": [
                    # "docker_shell_tool",
                    # "shell_tool"
                    "vector_store_query_tool",
                    "vector_store_add_docs_tool",
                    "vector_store_load_tool"
                ]
            },
            {"thread_id": 42}
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        break
