# Langgraph AI Terminal 🤖
#### By Ryan Eggleston [@ryaneggz](https://github.com/ryaneggz)

LangGraph Bot is a Python-based chatbot application that utilizes the LangGraph and LangChain libraries to process and respond to user inputs. The bot is designed to handle conversational flows and can be configured to use different language models.

## Features

- Stream processing of user inputs and bot responses.
- Visualization of state graphs using Mermaid.
- Configurable session management for chat history.
- Integration with OpenAI's GPT-4o, or Claude 3.5 Sonnet model.

## Prerequisites

- Python 3.10 or higher
- Access to OpenAI API (for GPT-4o model) or Anthropic API (for Claude 3.5 Sonnet)

## Installation

1. **Create a configuration directory:**

   ```bash
   ai --env
   ```

2. **Edit the env file:**

   ```bash
   nano $HOME/.ai-term/.env
   ```

## Usage

**Run the application:**

   To start the chatbot, run the following command:

   ```bash
   ai --help

   ### RESULT
   # usage: ai [-h] [--t TOOLS] [--ls] [--v] [--chat] [--id ID] [--env] [input ...]
   # AI CLI Tool
   # positional arguments:
   # input       Input text for the AI
   # options:
   # -h, --help  show this help message and exit
   # --t TOOLS   Comma-separated list of tools to use
   # --ls        List available tools
   # --v         Visualize the graph
   # --chat      Start an interactive chat session
   # --id ID     Thread ID for the conversation
   # --env       Create .env file in ~/.ai-term/
   ```
# Project Documentation

This project includes tools for running shell commands and Docker container operations. For detailed information, please refer to the following documentation:

- [Tools Documentation](./docs/tools.md)
- [Docker Compose Configuration](./docs/docker-compose.md)
- [Human-In-The-Loop](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent-hitl/#usage)


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.