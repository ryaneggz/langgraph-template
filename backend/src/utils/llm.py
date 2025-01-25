from enum import Enum
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

from src.constants import OLLAMA_BASE_URL, OPENAI_API_KEY, ANTHROPIC_API_KEY, GROQ_API_KEY
from src.constants.llm import ModelName
class LLMWrapper:
    def __init__(self, model_name: str, tools: list = None, **kwargs):
        self.model = None
        self.model_name = model_name
        self.kwargs = kwargs
        self.tools = tools
        self.choose_model(model_name)
        
    def __getattr__(self, item):
        # Redirect attribute access to the wrapped model
        return getattr(self.model, item)
        
    def choose_model(self, model_name: str):
        chosen_model = None

        if model_name not in [e.value for e in ModelName]:
            raise ValueError(f"Model {model_name} not supported")
        
        if 'openai' in model_name and OPENAI_API_KEY:
            self.kwargs['api_key'] = OPENAI_API_KEY
            model_name = model_name.replace('openai-', '')
            chosen_model = ChatOpenAI(model=model_name, **self.kwargs)
        elif 'anthropic' in model_name and ANTHROPIC_API_KEY:
            self.kwargs['api_key'] = ANTHROPIC_API_KEY
            model_name = model_name.replace('anthropic-', '')
            chosen_model = ChatAnthropic(model=model_name, **self.kwargs)
        elif 'ollama' in model_name and OLLAMA_BASE_URL:
            self.kwargs['base_url'] = OLLAMA_BASE_URL
            model_name = model_name.replace('ollama-', '')
            chosen_model = ChatOllama(model=model_name, **self.kwargs)
        elif 'groq' in model_name and GROQ_API_KEY:
            self.kwargs['api_key'] = GROQ_API_KEY
            model_name = model_name.replace('groq-', '')
            chosen_model = ChatGroq(model=model_name, **self.kwargs)
        else:
            raise ValueError(f"Provider {model_name} not supported")
            
        if self.tools and len(self.tools) > 0:
            self.model = chosen_model.bind_tools(tools=self.tools)
        else:
            self.model = chosen_model
            
    def embedding_model(self):
        chosen_model = None
        if 'openai' in self.model_name:
            model_name = self.model_name.replace('openai-', '')
            chosen_model = OpenAIEmbeddings(model=model_name, **self.kwargs)
        else:
            raise ValueError(f"Embedding model {model_name} not supported")
        return chosen_model
        
