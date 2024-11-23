import os
from langchain_core.messages import AIMessage, BaseMessage  
from langgraph.graph import END
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState

from src.utils.state import State, StateManager
from src.utils.llm import LLMWrapper, ModelName

llm = LLMWrapper(model_name=ModelName.ANTHROPIC, api_key=os.getenv("ANTHROPIC_API_KEY"))

local_store = {}

# Define the function that calls the model
def call_chat_model(state: MessagesState, config: RunnableConfig) -> list[BaseMessage]:
    # Make sure that config is populated with the session id
    if "configurable" not in config or "session_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
        )
    # Fetch the history of messages and append to it any new messages.
    state_manager = StateManager(config)
    messages = state_manager.collect_messages(local_store, state)
    ai_message = llm.invoke(messages)
    # Finally, update the chat message history to include
    # the new input message from the user together with the
    # repsonse from the model.
    state_manager.add_messages(local_store, messages + [ai_message])
    return {"messages": ai_message}

def error_node(state: State):
    return {"messages": [AIMessage(content="I'm sorry, I don't understand. Please try again.")]}

def should_run(state: State):
    return "call_chat_model" if 'please' in state["messages"][-1].content.lower() else END

def should_run(state: State):
    return "call_chat_model" if 'please' in state["messages"][-1].content.lower() else 'error'
