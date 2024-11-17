from typing_extensions import Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage

# store = {}

# def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = InMemoryHistory()
#     return store[session_id]


# history = get_by_session_id("1")
# history.add_message(AIMessage(content="hello"))

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You're an assistant who's good at {ability}"),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "{question}"),
# ])

# chain = prompt | ChatAnthropic(model="claude-3-sonnet-20240229")

# chain_with_history = RunnableWithMessageHistory(
#     chain,
#     # Uses the get_by_session_id function defined in the example
#     # above.
#     get_by_session_id,
#     input_messages_key="question",
#     history_messages_key="history",
# )