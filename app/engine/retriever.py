# retriever.py
from abc import ABC, abstractmethod
from typing import List
from app.engine.document import Document

class Retriever(ABC):
    @abstractmethod
    def get_relevant_documents(self, query: str) -> List[Document]:
        pass
