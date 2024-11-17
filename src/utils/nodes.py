# https://python.langchain.com/docs/versions/migrating_memory/chat_history/
import os
from langchain_core.messages import AIMessage, BaseMessage  
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState
from langchain_core.chat_history import InMemoryChatMessageHistory

from src.utils.state import State

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))


chats_by_session_id = {}
def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    chat_history = chats_by_session_id.get(session_id)
    if chat_history is None:
        chat_history = InMemoryChatMessageHistory()
        chats_by_session_id[session_id] = chat_history
    return chat_history

# Define the function that calls the model
def call_model(state: MessagesState, config: RunnableConfig) -> list[BaseMessage]:
    # Make sure that config is populated with the session id
    if "configurable" not in config or "session_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
        )
    # Fetch the history of messages and append to it any new messages.
    chat_history = get_chat_history(config["configurable"]["session_id"])
    messages = list(chat_history.messages) + state["messages"]
    ai_message = llm.invoke(messages)
    # Finally, update the chat message history to include
    # the new input message from the user together with the
    # repsonse from the model.
    chat_history.add_messages(state["messages"] + [ai_message])
    return {"messages": ai_message}

def error_node(state: State):
    return {"messages": [AIMessage(content="I'm sorry, I don't understand. Please try again.")]}

def should_run(state: State):
    return "call_model" if 'please' in state["messages"][-1].content.lower() else END

def should_run(state: State):
    return "call_model" if 'please' in state["messages"][-1].content.lower() else 'error'
