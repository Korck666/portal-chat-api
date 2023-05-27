# app/engine/document_descriptor.py
# this class should contain all the information needed to create a document instance
# we are using it to set up a document factory engine, se we can deal with different document types
# using the same interface

from app.engine.document_type import DocumentType
from app.engine.log_level import LogLevel
from dataclasses import dataclass
import Configuration

@dataclass
class DocumentDescriptor:
    doc_type: DocumentType
    doc_name: str
    doc_metadata: Configuration
    doc_log_level: LogLevel
    doc_kwargs: dict
    doc_hash: int

    @staticmethod
    def from_dict(doc_dict: dict):

        return DocumentDescriptor(
            doc_type=doc_dict['doc_type': DocumentType],
            doc_name=doc_dict['doc_name': str],
            doc_metadata=doc_dict['doc_metadata': Configuration],
            doc_log_level=doc_dict['doc_log_level': LogLevel] | LogLevel.INFO,
            doc_kwargs=doc_dict['doc_kwargs': dict] | {},
            doc_hash=hash((doc_dict['doc_type'], doc_dict['doc_name'], doc_dict['doc_metadata'],
                          doc_dict['doc_log_level'], doc_dict['doc_kwargs'])))
