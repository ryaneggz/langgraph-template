from langchain_core.tools import tool

from langchain_community.tools import ShellTool, StructuredTool
from langgraph.prebuilt import ToolNode

@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["sf", "san francisco"]:
        return "It's 60 degrees and foggy."
    else:
        return "It's 90 degrees and sunny."


@tool
def get_coolest_cities():
    """Get a list of coolest cities"""
    return "nyc, sf"

@tool
def shell_tool(commands: list[str]):
    """Run a shell commands. Commands is a list of strings, each representing a command to run. Avoid interactive commands."""
    shell_tool = ShellTool()
    output = shell_tool.run({"commands": commands})
    print(output)
    return output

@tool
def docker_shell_tool(commands: list[str]):
    """Run shell commands in a Docker container. Accepts multiple commands as a list of strings. 
    Each command is executed sequentially inside the specified container. Avoid interactive commands."""
    
    shell_tool = ShellTool()  # Initialize the ShellTool instance
    
    container_name = "ubuntu24"
    
    # Combine the docker execution command with each provided command
    docker_commands = [
        f'docker exec {container_name} bash -c "{command}"' for command in commands
    ]
    
    # Run the commands sequentially
    outputs = []
    for docker_command in docker_commands:
        output = shell_tool.run({"commands": [docker_command]})
        outputs.append(output)
        print(output)  # Optional: Log each command's output
    
    return outputs  # Return the output of all commands


tools = [get_weather, get_coolest_cities, shell_tool, docker_shell_tool]
tool_node = ToolNode(tools)