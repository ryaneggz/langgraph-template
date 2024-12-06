from enum import Enum
from typing import Optional, List, Any

from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage

from src.constants.examples import (
    THREAD_HISTORY_EXAMPLE,
    NEW_THREAD_ANSWER_EXAMPLE,
    EXISTING_THREAD_ANSWER_EXAMPLE,
    EXISTING_THREAD_QUERY_EXAMPLE,
    NEW_THREAD_QUERY_EXAMPLE
)


class Configurable(BaseModel):
    thread_id: str

class StreamInput(BaseModel):
    messages: list
    configurable: Configurable
    
class ExistingThread(BaseModel):
    query: str = Field(...)
    tools: Optional[List[Any]] = Field(default_factory=list)
    stream: Optional[bool] = Field(default=False)
    images: Optional[List[str]] = Field(default_factory=list)
    
    model_config = {
        "json_schema_extra": {"example": EXISTING_THREAD_QUERY_EXAMPLE}
    }
    
class NewThread(ExistingThread):
    system: Optional[str] = Field(default="You are a helpful assistant.")
    visualize: Optional[bool] = Field(default=False)
    
    model_config = {
        "json_schema_extra": {"example": NEW_THREAD_QUERY_EXAMPLE}
    }
        
class LLMHTTPResponse(BaseModel):
    thread_id: str = Field(...)
    messages: list[AnyMessage] = Field(default_factory=list)
    
    model_config = {
        "json_schema_extra": {
            "examples": {
                "thread_history": THREAD_HISTORY_EXAMPLE
            }
        }
    }
    
class Answer(BaseModel):
    thread_id: str = Field(...)
    answer: AnyMessage = Field(...)
    
    model_config = {
        "json_schema_extra": {
            "examples": {
                'new_thread': NEW_THREAD_ANSWER_EXAMPLE,
                'existing_thread': EXISTING_THREAD_ANSWER_EXAMPLE,
            }
        }
    }
        

    
##### Vector Store
class SearchType(str, Enum):
    MMR = "mmr"
    SIMILARITY = "similarity"

class SearchKwargs(dict):
    k: int = 3
    fetch_k: int = 2
    lambda_mult: float = 0.5
    filter: str = None