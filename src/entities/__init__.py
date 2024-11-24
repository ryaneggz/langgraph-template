from enum import Enum
from typing import Optional, List, Any

from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage


class Configurable(BaseModel):
    thread_id: str

class StreamInput(BaseModel):
    messages: list
    configurable: Configurable
    
class ExistingThread(BaseModel):
    query: str = Field(...)
    tools: Optional[List[Any]] = Field(default_factory=list)
    stream: Optional[bool] = Field(default=False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What about Germany?",
                "tools": [],
                "stream": False
            }
        }
    
class NewThread(ExistingThread):
    system: Optional[str] = Field(default="You are a helpful assistant.")
    visualize: Optional[bool] = Field(default=False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "system": "You are a helpful assistant.",
                "query": "What is the capital of France?",
                "tools": [],
                "stream": False,
                "visualize": False
            }
        }
        
class LLMHTTPResponse(BaseModel):
    thread_id: str = Field(...)
    messages: list[AnyMessage] = Field(default_factory=list)
    
    
##### Vector Store
class SearchType(str, Enum):
    MMR = "mmr"
    SIMILARITY = "similarity"

class SearchKwargs(dict):
    k: int = 3
    fetch_k: int = 2
    lambda_mult: float = 0.5
    filter: str = None