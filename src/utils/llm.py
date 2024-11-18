from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from src.utils.tools import tools

class ModelName(str, Enum):
    OPENAI = "openai-gpt-4o"
    ANTHROPIC = "anthropic-claude-3-5-sonnet-20240620"

class LLMWrapper:
    def __init__(self, model_name: str, tools: list = None, **kwargs):
        self.model = None
        self.kwargs = kwargs
        self.tools = tools
        self.choose_model(model_name)
        
    def __getattr__(self, item):
        # Redirect attribute access to the wrapped model
        return getattr(self.model, item)
        
    def choose_model(self, model_name: str):
        chosen_model = None
        if 'openai' in model_name:
            model_name = model_name.replace('openai-', '')
            chosen_model = ChatOpenAI(model=model_name, **self.kwargs)
        elif 'anthropic' in model_name:
            model_name = model_name.replace('anthropic-', '')
            chosen_model = ChatAnthropic(model=model_name, **self.kwargs)
            
        if self.tools and len(self.tools) > 0:
            self.model = chosen_model.bind_tools(tools=self.tools)
        else:
            self.model = chosen_model
        