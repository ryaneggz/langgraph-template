from enum import Enum

ROOT_PATH = './sandbox/system' 

class SystemPaths(Enum):
    DEFAULT = f"{ROOT_PATH}/default.txt"
    PIRATE = f"{ROOT_PATH}/pirate.txt"
    COT_MCTS = f"{ROOT_PATH}/cot.md"



# Read the 'system' message from a file
def read_system_message(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading system message file: {e}")
        return "You are a helpful AI assistant."