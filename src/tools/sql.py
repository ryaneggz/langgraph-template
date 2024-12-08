import os

from langchain_core.tools import tool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from src.constants import *
from src.utils.logger import logger
from src.utils.llm import LLMWrapper, ModelName

@tool
def sql_query_read(query: str):
    """Run a SQL query against a database.

    Args:
        query (str): SQL query string to execute

    Returns:
        dict: Response containing:
            - input: Original query string
            - output: Query execution results
            - intermediate_steps: Any intermediate processing steps
    """
    try:
        logger.info(f"Running READ SQL query: {query}")
        db = SQLDatabase.from_uri(DB_URI_SANDBOX, engine_args={"pool_size": 20})
        llm = LLMWrapper(
            model_name=ModelName.ANTHROPIC,
            api_key=ANTHROPIC_API_KEY, 
            tools=[]
        )
        toolkit = SQLDatabaseToolkit(db=db, llm=llm.model)
        agent = create_sql_agent(
            llm=llm.model, 
            toolkit=toolkit, 
            verbose=True if APP_LOG_LEVEL == "DEBUG" else False
        )
    
        response = agent.invoke(query)
        return response
    except Exception as e:
        logger.error(f"Error running SQL query: {str(e)}")
        raise e

@tool
def sql_query_write(query: str):
    """Run a SQL query against a database.

    Args:
        query (str): SQL query string to execute

    Returns:
        dict: Response containing:
            - input: Original query string
            - output: Query execution results
            - intermediate_steps: Any intermediate processing steps
    """
    try:
        logger.info(f"Running WRITE SQL query: {query}")
        db = SQLDatabase.from_uri(DB_URI_SANDBOX, engine_args={"pool_size": 20})
        llm = LLMWrapper(
            model_name=ModelName.ANTHROPIC,
            api_key=ANTHROPIC_API_KEY, 
            tools=[]
        )
        db_chain = SQLDatabaseChain.from_llm(llm.model, db)
    
        response = db_chain.invoke(query)
        return response
    except Exception as e:
        logger.error(f"Error running SQL query: {str(e)}")
        raise e