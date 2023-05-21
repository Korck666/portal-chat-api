# vector_database.py
from abc import abstractmethod
from typing import List, Tuple
from app.engine.database import Database
from app.engine.database_descriptor import DatabaseDescriptor


class VectorDatabase(Database):
    def __init__(self, descriptor: DatabaseDescriptor) -> None:
        super().__init__(descriptor)

    @abstractmethod
    def create_index(self, index_name: str, dimension: int, metric: str) -> 'VectorDatabase':
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    def insert(self, id: str, vector: List[float]):
        raise NotImplementedError

    @abstractmethod
    def query(self, vector: List[float], top_k: int) -> Tuple[List[str], List[float]]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError
