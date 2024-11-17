from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class LLMWrapper:
    def __init__(self, model_name: str, **kwargs):
        self.model = None
        self.kwargs = kwargs
        self.choose_model(model_name)
        
    def __getattr__(self, item):
        # Redirect attribute access to the wrapped model
        return getattr(self.model, item)
        
    def choose_model(self, model_name: str):
        if 'openai' in model_name:
            model_name = model_name.replace('openai-', '')
            self.model = ChatOpenAI(model=model_name, **self.kwargs)
        elif 'anthropic' in model_name:
            model_name = model_name.replace('anthropic-', '')
            self.model = ChatAnthropic(model=model_name, **self.kwargs)