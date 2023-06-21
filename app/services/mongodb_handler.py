# service/mongodb_handler.py
import logging


class MongoDBHandler(logging.Handler):
    def __init__(self, collection):
        logging.Handler.__init__(self)
        self.collection = collection

    def emit(self, record):
        # Insert a new document into the collection with the log record's attributes
        self.collection.insert_one(record.__dict__)
