# app/impl/databases/vector/descriptors/pinecone_descriptor.py
from dataclasses import dataclass
from app.engine.database_descriptor import DatabaseDescriptor
import Configuration


@dataclass
class PineconeDescriptor:
    api_key: str
    environment: str
    index_name: str
    host: str
    project_name: str
    log_level: str
    openapi_config: Configuration
    config: str
    kwargs: dict

    @staticmethod
    def from_database_descriptor(descriptor: DatabaseDescriptor,) -> 'PineconeDescriptor':
        return PineconeDescriptor(
            api_key=descriptor.api_key,
            environment=descriptor.environment,
            index_name=descriptor.db_name,
            host=descriptor.host,
            project_name='portal-chat-api',
            log_level=descriptor.log_level,
            openapi_config=descriptor.openapi_config,
            config=descriptor.config,
            kwargs=descriptor.kwargs
        )
