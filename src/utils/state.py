# https://python.langchain.com/docs/versions/migrating_memory/chat_history/
from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableConfig


class State(TypedDict):
    messages: Annotated[list, add_messages]
    session_id: str
    enabled: bool
    
class StateManager:
    def __init__(self, config: RunnableConfig):
        self.config = config
        self.session_id = config["configurable"]["session_id"]
        
    def get_chat_history(self, store: dict[str, InMemoryChatMessageHistory]) -> InMemoryChatMessageHistory:
        chat_history = store.get(self.session_id)
        if chat_history is None:
            chat_history = InMemoryChatMessageHistory()
            store[self.session_id] = chat_history
        return chat_history
    
    def collect_messages(self, store: dict[str, InMemoryChatMessageHistory], state: State) -> list[BaseMessage]:
        return list(self.get_chat_history(store).messages) + state["messages"]

    def add_messages(self, store: dict[str, InMemoryChatMessageHistory], messages: list[BaseMessage]):
        self.get_chat_history(store).add_messages(messages)
