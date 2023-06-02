# app/engine/document_descriptor.py
# this class should contain all the information needed to create a document instance
# we are using it to set up a document factory engine, se we can deal with different document types
# using the same interface

from app.engine.document_type import DocumentType
from app.engine.log_level import LogLevel
from dataclasses import dataclass
from app.engine.descriptor import Descriptor


@dataclass
class DocumentDescriptor(Descriptor):
    doc_type: DocumentType
    doc_name: str
    doc_metadata: dict
    doc_kwargs: dict

    def __init__(self, doc_type: DocumentType, doc_name: str,
                 doc_metadata: dict, doc_log_level: LogLevel = LogLevel.INFO,
                 doc_kwargs: dict = {}) -> None:
        super().__init__(log_level=doc_log_level)
        self.doc_type = doc_type
        self.doc_name = doc_name
        self.doc_metadata = doc_metadata
        self.doc_kwargs = doc_kwargs
        self.uid = self.generate_uid()

    @staticmethod
    def from_dict(doc_dict: dict):
        return DocumentDescriptor(
            doc_type=doc_dict['doc_type': DocumentType],
            doc_name=doc_dict['doc_name': str],
            doc_metadata=doc_dict['doc_metadata': dict],
            doc_log_level=doc_dict['doc_log_level': LogLevel] | LogLevel.INFO,
            doc_kwargs=doc_dict['doc_kwargs': dict] | {})
