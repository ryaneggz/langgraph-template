
from src.utils.stream import stream_graph_tokens
from src.flows.should_run_end import graph

# Chat loop
while True:
    try:
        user_input = input("\n>> User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_tokens(
            graph, 
            user_input,
            {
                "enabled": False,
                "session_id": "1"
            }
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        break