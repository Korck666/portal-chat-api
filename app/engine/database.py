# app/engine/database.py
from database_descriptor import DatabaseDescriptor
class Database:
    
    _instance = None

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance

    def __init__(self, db):
        self.db = Database()

    def connect(self):
        self.db.connect()

    def disconnect(self):
        self.db.disconnect()

    def query(self, query):
        return self.db.query(query)

