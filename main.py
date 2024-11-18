
from src.utils.stream import stream_graph_values
from src.flows.terminal_interact import graph
import traceback

# Chat loop
while True:
    try:
        user_input = input("\n>> User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # stream_graph_tokens(
        #     graph, 
        #     user_input,
        #     {
        #         "enabled": False,
        #         "session_id": "1"
        #     }
        # )
        stream_graph_values(
            graph,
            {
                "messages": [('human', user_input)], 
                "tools": [
                    "docker_shell_tool",
                    # "shell_tool"
                ]
            },
            {"thread_id": 42}
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        break
