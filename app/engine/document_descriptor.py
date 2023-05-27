# document_descriptor.py
# this class should contain all the information needed to create a document instance
# we are using it to set up a document factory engine, se we can deal with different document types
# using the same interface


from dataclasses import dataclass


@dataclass
class DocumentDescriptor:
    def __init__(self, *args, **kwargs) -> None:
        pass
    # Define your DocumentDescriptor class here
    pass
