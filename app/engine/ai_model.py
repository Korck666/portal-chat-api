# app/engine/ai_model.py
from abc import ABC, abstractmethod
from typing import Dict
from app.engine.ai_service import AIService


class AIModel(ABC):
    _models: Dict['AIService', 'AIModel'] = {}

    
    @abstractmethod
    def query(self, prompt: str) -> str:
        pass
