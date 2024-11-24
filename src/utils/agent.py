import os

from fastapi import status
from fastapi.responses import Response, JSONResponse
from psycopg_pool import ConnectionPool
from langgraph.graph import StateGraph
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from psycopg_pool import ConnectionPool

from src.utils.tools import collect_tools
from src.utils.llm import LLMWrapper, ModelName
from src.entities import LLMHTTPResponse
from src.utils.system import SystemPaths, read_system_message

class Agent:
    def __init__(self, thread_id: str, pool: ConnectionPool):
        self.connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        self.thread_id = thread_id
        self.config = {"configurable": {"thread_id": self.thread_id}}
        self.graph = None
        self.pool = pool
        
    def _checkpointer(self):
        checkpointer = PostgresSaver(self.pool)
        checkpointer.setup()
        return checkpointer
    
    def checkpoint(self):
        checkpointer = self._checkpointer()
        checkpoint = checkpointer.get(self.config)
        return checkpoint
        
    def builder(
        self,
        tools: list[str] = [],
        debug: bool = False
    ) -> StateGraph:
        llm = LLMWrapper(
            model_name=ModelName.ANTHROPIC,
            api_key=os.getenv("ANTHROPIC_API_KEY"), 
            tools=tools
        )
        checkpointer = self._checkpointer()
        tools = [] if len(tools) == 0 else collect_tools(tools)
        graph = create_react_agent(llm, tools=tools, checkpointer=checkpointer)
        if debug:
            graph.debug = True
        self.graph = graph
        return graph
        
    def process(
        self,
        messages: list[AnyMessage], 
        stream: bool = False,
    ) -> Response:
        if not stream:
            invoke = self.graph.invoke({"messages": messages}, {'configurable': {'thread_id': self.thread_id}})
            content = LLMHTTPResponse(
                thread_id=self.thread_id,
                messages=invoke.get('messages')
            ).model_dump()

            return JSONResponse(
                content=content,
                status_code=status.HTTP_200_OK
            )
            
        return JSONResponse(
            content={"error": "Streaming is not implemented yet."},
            status_code=status.HTTP_501_NOT_IMPLEMENTED
        )
        
    @staticmethod
    def messages(query: str, system: str = None) -> list[AnyMessage]:
        messages = [HumanMessage(content=query)]
        if not isinstance(messages[0], SystemMessage):
            if system:
                messages.insert(0, SystemMessage(content=system))
            else:
                messages.insert(0, SystemMessage(content=read_system_message(SystemPaths.COT_MCTS.value)))
        return messages