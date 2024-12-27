from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
class Config(BaseModel):
    llm: BaseChatModel

def create_chatbot(config: Config):
    def chatbot(state: State):
        model: BaseChatModel = config.get('model')
        return {"messages": [model.invoke(state["messages"])]}
    return chatbot

def chatbot_builder(config: Config):
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", create_chatbot(config))
    graph_builder.set_entry_point("chatbot")
    graph_builder.set_finish_point("chatbot")
    return graph_builder