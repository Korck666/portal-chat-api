from typing import List, Tuple
from pinecone import Index
from app.engine.vector_database import VectorDatabase

class PineconeDatabase(VectorDatabase):
    def __init__(self, index_name: str):
        super().__init__()
        self.index = Index(index_name=index_name)

    def connect(self):
        self.index.create()

    def disconnect(self):
        self.index.delete()

    def insert(self, id: str, vector: List[float]):
        self.index.upsert(items={id: vector})

    def query(self, vector: List[float], top_k: int) -> Tuple[List[str], List[float]]:
        results = self.index.query(queries=[vector], top_k=top_k)
        return results.ids[0], results.scores[0]

    def delete(self, id: str):
        self.index.delete(ids=[id])
