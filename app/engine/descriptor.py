# app/engine/descriptor.py
from dataclasses import dataclass
from typing import Any
import hashlib
from app.engine.log_level import LogLevel


@dataclass
class Descriptor:
    doc_log_level: LogLevel

    def __init__(self, log_level: LogLevel) -> None:
        self.log_level = log_level
        self.uid = self.generate_uid()

    def generate_uid(self) -> str:
        # Concatenate all properties of the descriptor
        properties = "".join(str(value) for value in self.__dict__.values())
        # Generate a hash of the properties
        self.uid = hashlib.sha256(properties.encode()).hexdigest()
        return self.uid

    def properties(self) -> Any:
        return self.__dict__.values()
