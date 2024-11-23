# LangGraph Bot

LangGraph Bot is a Python-based chatbot application that utilizes the LangGraph and LangChain libraries to process and respond to user inputs. The bot is designed to handle conversational flows and can be configured to use different language models.

## Features

- Stream processing of user inputs and bot responses.
- Visualization of state graphs using Mermaid.
- Configurable session management for chat history.
- Integration with OpenAI's GPT-4o model.

## Prerequisites

- Python 3.8 or higher
- Access to OpenAI API (for GPT-4o model)

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

   Create a `.env` file in the root directory and add your OpenAI API key:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

   Ensure that your `.env` file is not tracked by git by checking the `.gitignore`:

   ```gitignore
   startLine: 1
   endLine: 1
   ```

## Usage

**Run the application:**

   To start the chatbot, run the following command:

   ```bash
   python main.py
   ```

   The bot will start a chat loop where you can input messages. Type "quit", "exit", or "q" to end the session.

# Project Documentation

This project includes tools for running shell commands and Docker container operations. For detailed information, please refer to the following documentation:

- [Tools Documentation](./docs/tools.md)
- [Docker Compose Configuration](./docs/docker-compose.md)
- [Human-In-The-Loop](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent-hitl/#usage)