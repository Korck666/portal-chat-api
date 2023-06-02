# app/impl/service/ai/openai_service.py
from app.engine.ai_service import AIService
from app.engine.ai_service_descriptor import AIServiceDescriptor
from app.engine.ai_model import AIModel
from app.impl.service.ai.openai_model import OpenAIModel
import openai
from typing import Dict


class OpenAIService(AIService):
    def __init__(self, descriptor: AIServiceDescriptor) -> None:
        super().__init__(descriptor)

    def connect(self) -> None:
        openai.api_key = self.descriptor.api_key

    def add_model(self, model_name: str) -> None:
        self.models[model_name] = OpenAIModel(model_name)

    @classmethod
    def getModels(cls) -> Dict[str, AIModel]:
        return cls.models
