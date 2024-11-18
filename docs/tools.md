# Tools Documentation
## shell_tool
The `shell_tool` is a function that allows running shell commands. It accepts a list of strings, where each string represents a command to be executed.
### Parameters
- `commands`: A list of strings, each representing a shell command to be executed.
### Usage
```python
from src.utils.tools import shell_tool

result = shell_tool(["ls -l", "pwd"])
print(result)
```

## docker_shell_tool
The `docker_shell_tool` is a function that allows running shell commands inside a Docker container. It accepts a list of strings, where each string represents a command to be executed in the container.
### Parameters
- `commands`: A list of strings, each representing a shell command to be executed in the Docker container.
### Usage
```python
from src.utils.tools import docker_shell_tool

result = docker_shell_tool(["ls -l", "pwd"])
print(result)
```

