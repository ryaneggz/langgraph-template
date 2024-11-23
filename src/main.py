import traceback
import argparse
import sys
import os
import shutil

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

from src.flows.chat_agent import builder
from src.utils.stream import stream_graph_values
from src.utils.system import read_system_message, SystemPaths
from src.utils.tools import tools
from src.utils.visualize import visualize_graph

def list_available_tools():
    available_tools = [ t.name for t in tools ]
    print("\nAvailable tools:")
    for tool in available_tools:
        print(f"- {tool}")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='AI CLI Tool by Ryan Eggleston (Github: ryaneggz)')
    parser.add_argument('input', nargs='*', help='Input text for the AI')
    parser.add_argument('--t', dest='tools', help='Comma-separated list of tools to use')
    parser.add_argument('--ls', action='store_true', help='List available tools')
    parser.add_argument('--v', action='store_true', help='Visualize the graph')
    parser.add_argument('--chat', action='store_true', help='Start an interactive chat session')
    parser.add_argument('--id', type=int, default=42, help='Thread ID for the conversation')
    parser.add_argument('--env', action='store_true', help='Create .env file in ~/.ai-term/')
    args = parser.parse_args()

    if args.env:
        # Create ~/.ai-term directory if it doesn't exist
        ai_lib_dir = os.path.expanduser("~/.ai-term")
        os.makedirs(ai_lib_dir, exist_ok=True)
        
        # Copy .example.env to ~/.ai-term/.env
        example_env_path = os.path.join(os.path.dirname(__file__), '.example.env')
        env_path = os.path.join(ai_lib_dir, ".env")
        shutil.copy2(example_env_path, env_path)
        print(f"\nCreated environment file at: {env_path}")
        print("Please edit this file with your API keys and other configuration.")
        sys.exit(0)

    # Load .env from ~/.ai-term/.env
    env_path = os.path.expanduser("~/.ai-term/.env")
    load_dotenv(env_path)

    if args.ls:
        list_available_tools()

    # Initialize graph
    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    
    # Only visualize if --v flag is passed
    if args.v:
        visualize_graph(graph, "chat_agent")

    tools = []
    if args.tools:
        tools = [t.strip() for t in args.tools.split(',')]

    try:
        if args.chat:
            print("\nStarting chat session (type 'quit', 'exit', or 'q' to end)")
            while True:
                user_input = input("\n>> Query: ")
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
                        "tools": tools if tools else []
                    },
                    {"thread_id": args.id}
                )
        else:
            user_input = ' '.join(args.input) if args.input else input("\n>> Query: ")
            
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
                    "tools": tools if tools else []
                },
                {"thread_id": args.id}
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
