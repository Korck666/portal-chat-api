# retriever.py
from typing import List

class Retriever(ABC):
    @abstractmethod
    def get_relevant_documents(self, query: str) -> List[Document]:
        pass
