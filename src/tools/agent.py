from langchain_core.tools import tool

from psycopg_pool import ConnectionPool
from src.constants import DB_URI, CONNECTION_POOL_KWARGS

@tool
def available_tools():
    """List all available tools."""
    from src.tools import tools
    return [tool.name for tool in tools]

@tool
def agent_builder(thread_id: str, query: str, system: str, tools: list[str]):
    """Build and run an AI agent with the specified configuration.
    
    Args:
        thread_id (str): Unique identifier for the conversation thread
        query (str): The user's question or request to be processed
        system (str): System message to set context and instructions for the agent
        tools (list[str]): List of tool names the agent should have access to
        
    Returns:
        Response: JSON response containing the agent's answer and thread_id
        
    Example:
        .. code-block:: python
        
            response = agent_builder(
                thread_id="123e4567-e89b-12d3-a456-426614174000",
                query="What is the weather today?",
                system="You are a helpful weather assistant.",
                tools=["weather_query"]
            )
    """
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        from src.utils.agent import Agent
        agent = Agent(thread_id, pool)
        agent.builder(tools=tools)
        messages = agent.messages(query, system)
        response = agent.process(messages, False)
        return response