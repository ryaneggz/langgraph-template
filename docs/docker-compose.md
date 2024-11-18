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

This configuration sets up an Ubuntu 24.04 container named "ubuntu24" that runs continuously, allowing for command execution using the `docker_shell_tool`.
