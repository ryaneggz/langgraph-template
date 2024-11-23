import traceback
import argparse
import sys

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

from src.flows.chat_agent import builder
from src.utils.stream import stream_graph_values
from src.utils.system import read_system_message, SystemPaths
from src.utils.visualize import visualize_graph

def list_available_tools():
    tools = [
        "docker_shell_tool",
        "shell_tool",
        "vector_store_query_tool", 
        "vector_store_add_docs_tool",
        "vector_store_load_tool"
    ]
    print("\nAvailable tools:")
    for tool in tools:
        print(f"- {tool}")
    sys.exit(0)

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description='AI CLI Tool')
    parser.add_argument('input', nargs='*', help='Input text for the AI')
    parser.add_argument('--tools', help='Comma-separated list of tools to use')
    parser.add_argument('--ls', action='store_true', help='List available tools')
    args = parser.parse_args()

    if args.ls:
        list_available_tools()

    # Initialize graph and visualize once at start
    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    visualize_graph(graph, "chat_agent")

    tools = []
    if args.tools:
        tools = [t.strip() for t in args.tools.split(',')]

    try:
        user_input = ' '.join(args.input) if args.input else input("\n>> User: ")
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            return

        stream_graph_values(
            graph,
            {
                "system": read_system_message(SystemPaths.COT_MCTS.value),
                "messages": [
                    ('human', user_input)
                ],
                "tools": tools if tools else [
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

if __name__ == "__main__":
    main()
