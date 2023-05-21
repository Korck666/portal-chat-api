# database_descriptor.py
from enum import Enum

class DatabaseType(Enum):
    VECTOR = "VECTOR"
    SQL = "SQL"

class DatabaseDescriptor:
    def __init__(self, db_type: DatabaseType, api_key: str, environment: str, index_name: str, namespace: str):
        self.db_type = db_type
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self.namespace = namespace
