from langchain_core.tools import tool
from langchain_core.documents import Document

from src.utils.retrieval import VectorStore
from src.constants import DEFAULT_VECTOR_STORE_PATH

@tool
def retrieval_query(query: str, search_type: str = "similarity", search_kwargs: dict = {"k": 10}):
    """Query the vector store. Search type can be 'mmr' or 'similarity'. Search kwargs is a dictionary of kwargs for the search type."""
    loaded_vector_store = VectorStore().load_vector_store()
    vector_store = VectorStore(loaded_vector_store)
    return vector_store.retrieve(query, search_type, search_kwargs)

@tool
def retrieval_add(docs: list[Document]):
    """Add documents to the vector store.
    
    Example:

        .. code-block:: python

            from langchain_core.documents import Document

            document = Document(
                page_content="Hello, world!",
                metadata={"source": "https://example.com"}
            )
    """
    return VectorStore().add_docs(docs)

@tool
def retrieval_load(path: str = DEFAULT_VECTOR_STORE_PATH):
    """Load the vector store from a file."""
    vector_store = VectorStore()
    return vector_store.load_vector_store(path)