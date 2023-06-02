# app/engine/ai_service_descriptor.py
from dataclasses import dataclass
from app.engine.descriptor import Descriptor
from app.engine.log_level import LogLevel


@dataclass
class AIServiceDescriptor(Descriptor):
    service_name: str
    api_key: str
    organization_key: str

    def __init__(self, service_name: str, api_key: str, organization_key: str,
                 log_level: LogLevel = LogLevel.INFO) -> None:
        super().__init__(log_level=log_level)
        self.service_name = service_name
        self.api_key = api_key
        self.organization_key = organization_key
        self.uid = self.generate_uid()

    @staticmethod
    def from_dict(service_dict: dict):
        return AIServiceDescriptor(
            service_name=service_dict['service_name': str],
            api_key=service_dict['api_key': str],
            organization_key=service_dict['organization_key': str],
            log_level=service_dict['log_level': LogLevel] | LogLevel.INFO)
