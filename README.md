# Graph Agent Template 🤖

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

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ryaneggz/langgraph-template.git
   cd langgraph-template
   ```

2. **Set up a virtual environment using `uv venv`:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables:**

   Create a `.env` file in the root directory and add your API key(s):

   ```bash
   cp .example.env .env
   ```

   Ensure that your `.env` file is not tracked by git by checking the `.gitignore`:

## Usage

**Run the application:**

   To start the chatbot, run the following command:

   ```bash
   source .env && python main.py
   ```

   The bot will start a chat loop where you can input messages. Type "quit", "exit", or "q" to end the session.

# Project Documentation

This project includes tools for running shell commands and Docker container operations. For detailed information, please refer to the following documentation:

- [Tools Documentation](./docs/tools.md)
- [Docker Compose Configuration](./docs/docker-compose.md)
- [Human-In-The-Loop](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent-hitl/#usage)