import os
from enum import Enum
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document


def get_embedding_model():
    from src.utils.llm import LLMWrapper
    llm = LLMWrapper(model_name="openai-text-embedding-3-large", api_key=os.getenv('OPENAI_API_KEY'))
    return llm.embedding_model()

def get_vector_store():
    embedding_model = get_embedding_model()
    return InMemoryVectorStore(embedding_model)

class SearchType(str, Enum):
    MMR = "mmr"
    SIMILARITY = "similarity"
    
class SearchKwargs(dict):
    k: int = 3
    fetch_k: int = 2
    lambda_mult: float = 0.5
    filter: str = None

DEFAULT_VECTOR_STORE_PATH = './sandbox/db/vectorstore.json'

class VectorStore:
    def __init__(self, vector_store: InMemoryVectorStore = None):
        self.vector_store = vector_store if vector_store else get_vector_store()
        
    def load_vector_store(self, path: str = DEFAULT_VECTOR_STORE_PATH):
        try:
            store = self.vector_store.load(path, embedding=get_embedding_model())
            self.vector_store = store
        except Exception as e:
            print(f"Error loading vector store: {e}")
            raise e
        finally:
            return self.vector_store
        
    def add_docs(self, docs: list[Document]):
        self.vector_store.add_documents(docs)
        self.vector_store.dump(DEFAULT_VECTOR_STORE_PATH)
        return True
        
    async def aadd_docs(self, docs: list[Document]):
        await self.vector_store.aadd_documents(docs)
        return True
        
    def delete_docs(self, ids: list[str]):
        self.vector_store.delete(ids)
        return True
    
    async def adelete_docs(self, ids: list[str]):
        await self.vector_store.adelete(ids)
        return True
    
    def query(self, query: str, k: int = 3):
        return self.vector_store.similarity_search(query, k)
    
    def query_with_score(self, query: str, k: int = 3):
        return self.vector_store.similarity_search_with_score(query, k)
    
    async def aquery(self, query: str, k: int = 3):
        return await self.vector_store.asimilarity_search(query, k)
    
    async def aquery_with_score(self, query: str, k: int = 3):
        return await self.vector_store.asimilarity_search_with_score(query, k)
    
    def retrieve(self, 
        query: str, 
        search_type: str = "mmr",  
        search_kwargs: dict = None,
    ):
        retriever = self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs,
        )
        results = retriever.invoke(query)
        return results
    
    def find_docs_by_ids(self, ids: list[str]):
        return self.vector_store.get_by_ids(ids)