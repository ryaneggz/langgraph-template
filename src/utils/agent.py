import os
import base64
import requests
from typing import Optional

from fastapi import status
from fastapi.responses import Response, JSONResponse, StreamingResponse
from psycopg_pool import ConnectionPool
from langgraph.graph import StateGraph
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from psycopg_pool import ConnectionPool

from src.constants import APP_LOG_LEVEL
from src.tools import collect_tools
from src.utils.llm import LLMWrapper, ModelName
from src.entities import Answer
from src.utils.logger import logger
from src.utils.stream import stream_chunks

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
        debug: bool = True if APP_LOG_LEVEL == "DEBUG" else False
    ) -> StateGraph:
        llm = LLMWrapper(
            model_name=ModelName.ANTHROPIC,
            api_key=os.getenv("ANTHROPIC_API_KEY"), 
            tools=[]
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
        content_type: str = "application/json",
    ) -> Response:
        if content_type == "application/json":
            invoke = self.graph.invoke({"messages": messages}, {'configurable': {'thread_id': self.thread_id}})
            content = Answer(
                thread_id=self.thread_id,
                answer=invoke.get('messages')[-1]
            ).model_dump()

            return JSONResponse(
                content=content,
                status_code=status.HTTP_200_OK
            )
            
        # Assume text/event-stream for streaming
        def stream_generator():
            try:
                for chunk in stream_chunks(self.graph, messages, self.thread_id):
                    if chunk:
                        print(chunk)
                        yield chunk
            finally:
                # Ensure pool is closed after streaming is complete
                if not self.pool.closed:
                    self.pool.close()

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream"
        )
        
    @staticmethod
    def _get_base64_image(image_url: str) -> Optional[str]:
        """Fetch image from URL and convert to base64, or return existing base64 string."""
        # Check if the string is already a base64 data URL
        if image_url.startswith('data:image/'):
            return image_url
        
        # Check if it's a raw base64 string
        try:
            # Try to decode to check if it's valid base64
            base64.b64decode(image_url)
            # If successful, assume it's an image and add data URL prefix
            return f"data:image/png;base64,{image_url}"
        except Exception:
            # Not base64, try to fetch as URL
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                image_data = response.content
                base64_image = base64.b64encode(image_data).decode('utf-8')
                # Detect content type from response headers or default to png
                content_type = response.headers.get('content-type', 'image/png')
                return f"data:{content_type};base64,{base64_image}"
            except Exception as e:
                logger.error(f"Failed to fetch or encode image {image_url}: {str(e)}")
                return None

    @staticmethod
    def messages(
        query: str, 
        system: str = None, 
        images: list[str] = None,
        base64_encode: bool = True
    ) -> list[AnyMessage]:
        # Create message content based on whether images are present
        if images:
            content = [
                {"type": "text", "text": query}
            ]
            
            for image in images:
                if base64_encode:
                    encoded_image = Agent._get_base64_image(image)
                    if encoded_image:  # Only add if encoding was successful
                        content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": encoded_image,
                                "detail": "auto"
                            }
                        })
                else:
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": image,
                            "detail": "auto"
                        }
                    })
        else:
            content = query

        messages = [HumanMessage(content=content)]
        
        if not isinstance(messages[0], SystemMessage):
            if system:
                messages.insert(0, SystemMessage(content=system))
        return messages