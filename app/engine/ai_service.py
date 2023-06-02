# app/engine/ai_service.py
from app.engine.ai_service_descriptor import AIServiceDescriptor
from abc import ABC, abstractmethod
from typing import Dict
from app.engine.ai_model import AIModel
from app.engine.ai_service_type import AIServiceType
from app.engine.ai_model_descriptor import AIModelDescriptor


class AIService(ABC):
    __services: Dict[str, 'AIService'] = {}

    def __init__(self, descriptor: AIServiceDescriptor) -> None:
        self.descriptor = descriptor

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def add_model(self, model_descriptor: AIModelDescriptor) -> None:
        pass

    @staticmethod
    def get_instance(ai_type: AIServiceType, descriptor: AIServiceDescriptor = AIServiceDescriptor()):
        if ai_type not in Database._instances:
            if descriptor is None:
                raise ValueError(
                    f"No instance of {db_type} found and no descriptor provided to create one.")
            Database._instances[db_type] = db_type.create_instance(descriptor)
        return Database._instances[db_type]

    @staticmethod
    def list(db_type=None):
        if db_type is None:
            return list(Database._instances.keys())
        else:
            return [key for key in Database._instances.keys() if key == db_type]

    @classmethod
    def create_instance(cls, descriptor):
        raise NotImplementedError(
            "This method should be overridden in subclass")
