# Shell Docker

## shell_docker
The `shell_docker` is a function that allows running shell commands inside a Docker container. It accepts a list of strings, where each string represents a command to be executed in the container.

### Parameters
- `commands`: A list of strings, each representing a shell command to be executed in the Docker container.

### Usage
```python
@tool
def shell_docker(commands: list[str]):
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
```

# Docker Compose Configuration
The project uses Docker Compose to manage the containerized environment. Below is the configuration:

```yaml
version: "3"
services:
  ubuntu24:
    image: ubuntu:24.04
    container_name: ubuntu24
    command: tail -f /dev/null
```

This configuration sets up an Ubuntu 24.04 container named "ubuntu24" that runs continuously, allowing for command execution using the `shell_docker`.
