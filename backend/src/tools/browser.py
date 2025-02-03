import json
import uuid

from langchain_core.tools import tool, ToolException
from browser_use import Agent
from src.utils.llm import LLMWrapper
from src.utils.logger import logger

@tool
async def browser_use(task: str, model: str = "openai-gpt-4o"):
    """Use the browser to perform a task.
    
    Example:
        .. code-block:: python
        
            response = browser_use(
                task="Go to Reddit, search for 'browser-use', click on the first post and return the first comment.",
            )
    
    Args:
        task (str): The task to be performed
        
    Returns:
        Response: The result of the task
    """
    try:
        agent = Agent(
            task=task,
            llm=LLMWrapper(model=model),
        )
        result = await agent.run()
        return result
    except Exception as e:
        logger.error(f"Error in browser_use: {str(e)}")
        raise ToolException(f"Error running browser_use: {str(e)}")