# app/impl/pinecone_database.py
from abc import abstractmethod
from typing import List
import pinecone
from app.engine.vector_database import VectorDatabase
from app.engine.document import Document
from app.engine.database_descriptor import DatabaseDescriptor


class PineconeDatabase(VectorDatabase):
    def __init__(self, descriptor: DatabaseDescriptor):
        super().__init__(descriptor)
        self.pinecone_descriptor = PineconeVectorDatabase.from_database_descriptor(
            descriptor)

    @classmethod
    def create_instance(cls, descriptor):
        return cls(descriptor)

    @abstractmethod
    def connect(self):
        pinecone.init(
            **PineconeVectorDatabase.from_database_descriptor(self.descriptor))
        if self.pinecone_descriptor.index_name not in pinecone.list_indexes():
            raise ValueError(f"Index {self.index_name} not found.")
        self.index = pinecone.Index(index_name=self.index_name)

    @abstractmethod
    def create_index(self, index_name: str, dimension: int, metric: str) -> VectorDatabase:
        pinecone.create_index(index_name, dimension=dimension, metric=metric)
        return self

    @abstractmethod
    def disconnect(self):
        if self.index_name in pinecone.list_indexes():
            pinecone.delete_index(self.index_name)
        self.index = None

    @abstractmethod
    def insert(self, id: str, vector: List[float]):
        response = self.index.upsert(items={id: vector},)

    @abstractmethod
    def query(self, vector: List[float], top_k: int):
        results = self.index.query(queries=[vector], top_k=top_k)
        return results.ids[0], results.scores[0]

    @abstractmethod
    def delete(self, id: str):
        self.index.delete(ids=[id])
