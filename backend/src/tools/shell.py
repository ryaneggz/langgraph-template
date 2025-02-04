from langchain_core.tools import tool
from langchain_community.tools import ShellTool

from src.constants import SHELL_REMOTE_SERVER_URL
from src.utils.logger import logger


@tool
def shell_local(commands: list[str]):
    """Run a shell commands. Commands is a list of strings, each representing a command to run. Avoid interactive commands."""
    shell_tool = ShellTool()
    output = shell_tool.run({"commands": commands})
    logger.debug(output)
    return output

@tool
def shell_docker(commands: list[str], container_name: str = "ubuntu24"):
    """Run shell commands in a Docker container. Accepts multiple commands as a list of strings. 
    Each command is executed sequentially inside the specified container. Avoid interactive commands."""
    
    shell_tool = ShellTool()  # Initialize the ShellTool instance
    
    # Combine the docker execution command with each provided command
    docker_commands = [
        f'docker exec {container_name} bash -c "{command}"' for command in commands
    ]
    
    # Run the commands sequentially
    outputs = []
    for docker_command in docker_commands:
        output = shell_tool.run({"commands": [docker_command]})
        outputs.append(output)
        logger.debug(output)  # Optional: Log each command's output
    
    return outputs  # Return the output of all commands

@tool
def shell_exec(commands: list[str]):
    """Run shell commands in a remote server. Accepts multiple commands as a list of strings. 
    Each command is executed sequentially inside the specified container. Avoid interactive commands."""
    import requests
    
    # Run the commands sequentially
    outputs = []
    
    for command in commands:
        response = requests.post(SHELL_REMOTE_SERVER_URL, json={"cmd": command})
        output = response.text
        outputs.append(output)
        logger.debug(output)  # Optional: Log each command's output
    
    return outputs  # Return the output of all commands