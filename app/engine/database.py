# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    _instance = None

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance

    def __init__(self):
        self.engine = create_engine('postgresql://user:password@localhost/dbname')
        self.Session = sessionmaker(bind=self.engine)
