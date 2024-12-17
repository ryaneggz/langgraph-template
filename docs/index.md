# Thread Agent Documentation

Welcome to the Thread Agent documentation. This is a FastAPI-based application that integrates LangGraph for building sophisticated chatbot interactions.

## Overview

The Thread Agent is a powerful chatbot application that:
- Processes and responds to user inputs using LangGraph and LangChain
- Supports multiple language models (Claude 3.5 Sonnet and GPT-4)
- Provides document management and vector storage capabilities
- Includes tools for shell commands and Docker operations

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Access to OpenAI API or Anthropic API
- Docker and Docker Compose (for full functionality)

## API Reference

The [API documentation](/api) is available at `/api` when running the application. This includes:
- Complete endpoint documentation
- Request/response examples
- Authentication requirements

### Installation

1. Clone the repository:

```bash
git clone https://github.com/ryaneggz/langgraph-template.git
cd langgraph-template
```

2. Set up your virtual environment:

```bash
## Install uv if do not have
curl -LsSf https://astral.sh/uv/install.sh | sh

## Start venv
uv venv

## Activate
source .venv/bin/activate

## Install
uv pip install -r requirements.txt
```


## Core Features

### Document Management
The application provides comprehensive document management capabilities through the following endpoints:

### Available Tools
The system includes various tools for:
- Shell command execution
- Docker container management
- File processing and document handling

For detailed information about available tools, see the [Tools Documentation](tools/tools.md).

## Deployment

The application can be deployed using:
- Docker Compose for local development
- DigitalOcean for production deployment

For detailed deployment instructions, see the [Deployment Guide](deploy/digitalocean.md).

## Configuration

Environment variables can be configured through `.env` files:
- `.env` for local development
- `.env.production` for production settings

## Contributing

For contribution guidelines and development setup, please refer to our [GitHub repository](https://github.com/ryaneggz/langgraph-template).