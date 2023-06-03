# services/mongodb.py
from typing import Any, Generator
from pymongo import MongoClient
from utils.config import MDB_USERS, MDB_LOGS, MONGO_URL, MDB_DATABASE

client = MongoClient(host=MONGO_URL)
db = client[MDB_DATABASE]

collections: dict = dict({MDB_LOGS: db[MDB_LOGS], MDB_USERS: db[MDB_USERS]})

def get_database(client: MongoClient = client, database_name: str = MDB_DATABASE) -> Generator:
    db = client[database_name]
    yield db
