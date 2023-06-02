# app/engine/ai_model_descriptor.py
from dataclasses import dataclass
from app.engine.descriptor import Descriptor
from app.engine.log_level import LogLevel


@dataclass
class AIModelDescriptor(Descriptor):
    name: str
    default_temperature: float
    default_top_p: float
    # Add other parameters as needed

    def __init__(self, name: str, default_temperature: float = 0.3,
                 default_top_p: float = 1.0, log_level: LogLevel = LogLevel.INFO) -> None:
        super().__init__(log_level=log_level)
        self.name = name
        self.default_temperature = default_temperature
        self.default_top_p = default_top_p
        self.uid = self.generate_uid()

    @staticmethod
    def from_dict(model_dict: dict):
        return AIModelDescriptor(
            name=model_dict['name': str],
            default_temperature=model_dict['default_temperature': float] | 0.3,
            default_top_p=model_dict['default_top_p': float] | 1.0,
            log_level=model_dict['log_level': LogLevel] | LogLevel.INFO)
