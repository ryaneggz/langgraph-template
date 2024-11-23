import os
from enum import Enum
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

from utils.llm import LLMWrapper, ModelName

llm = LLMWrapper(api_key=os.getenv('OPENAI_API_KEY'))
embedding_model = llm.embedding_model(ModelName.OPENAI_EMBEDDING)
vector_store = InMemoryVectorStore(embedding_model)

class SearchType(str, Enum):
    MMR = "mmr"
    SIMILARITY = "similarity"
    
class SearchKwargs(dict):
    k: int = 3
    fetch_k: int = 2
    lambda_mult: float = 0.5
    filter: str = None

class VectorStore:
    def __init__(self):
        self.vector_store = vector_store
        
    def add_docs(self, docs: list[Document]):
        self.vector_store.add_documents(docs)
        
    async def aadd_docs(self, docs: list[Document]):
        await self.vector_store.aadd_documents(docs)
        
    def delete_docs(self, ids: list[str]):
        self.vector_store.delete(ids)
        
    async def adelete_docs(self, ids: list[str]):
        await self.vector_store.adelete(ids)
        
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
        retriever = vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs,
        )
        results = retriever.invoke(query)
        return results
    
    def find_docs_by_ids(self, ids: list[str]):
        return self.vector_store.get_by_ids(ids)