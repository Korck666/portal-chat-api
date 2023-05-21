from abc import abstractmethod
from typing import List
from app.engine.vector_database import VectorDatabase
from app.engine.retriever import Retriever
from app.engine.document import Document


class VectorDatabaseRetriever(Retriever):
    def __init__(self, vector_database: VectorDatabase):
        self.vector_database = vector_database

    def get_relevant_documents(self, query: str) -> List[Document]:
        # Convert the query to a vector using your chosen method
        query_vector = self.convert_query_to_vector(query)

        # Query the vector database
        document_ids, _ = self.vector_database.query(
            vector=query_vector, top_k=10)

        # Fetch the documents from your document store using the returned IDs
        documents = self.fetch_documents(document_ids)

        return documents

    @abstractmethod
    def convert_query_to_vector(self, query: str) -> List[float]:
        # Implement this method based on your specific requirements
        raise NotImplementedError

    @abstractmethod
    def fetch_documents(self, document_ids: List[str]) -> List[Document]:
        # Implement this method based on your specific requirements
        raise NotImplementedError
