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

1. **Run the application:**

   To start the chatbot, run the following command:

   ```bash
   python main.py
   ```

   The bot will start a chat loop where you can input messages. Type "quit", "exit", or "q" to end the session.

2. **Debugging:**

   If you are using VSCode, you can use the provided launch configuration to debug the application:

   ```json:.vscode/launch.json
   startLine: 1
   endLine: 14
   ```

## Development

- **Visualizing Graphs:**

  The application can visualize state graphs using the `visualize_graph` function:

  ```python:src/utils/visualize.py
  startLine: 1
  endLine: 19
  ```

- **Stream Processing:**

  The `stream_graph_tokens` function handles the streaming of user inputs and bot responses:

  ```python:src/utils/stream.py
  startLine: 25
  endLine: 36
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
