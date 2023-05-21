# vector_database.py
from abc import ABC, abstractmethod
from typing import List, Tuple
from app.engine.database import Database

class VectorDatabase(Database, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def insert(self, id: str, vector: List[float]):
        pass

    @abstractmethod
    def query(self, vector: List[float], top_k: int) -> Tuple[List[str], List[float]]:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass
