"""
This module contains a singleton class for MongoDB connection and collections.
"""
from functools import lru_cache
from pymongo import MongoClient
from typing import Any, Dict, Generator

from utils.config import Config


class MongoDB:
    """
    Singleton class for MongoDB connection and collections.
    """

    _instance = None

    def __new__(cls) -> "MongoDB":
        """
        Singleton implementation for class MongoDB.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """
        Initializes MongoDB connection and collections.
        """
        self.config = Config()
        self.client = MongoClient(host=self.config.MONGODB_URL)
        self.db = self.client[self.config.MONGODB_DB]
        self.collections: Dict[Any, Any] = {
            self.config.DB_LOGS: self.db[self.config.DB_LOGS],
            self.config.DB_LOGS: self.db[self.config.DB_USERS],
        }
        # cache the get_user method
        self.get_user = lru_cache()(self.__get_user)

    def __get_user(self, user_id: str) -> Any:
        # TODO: implement the get_user method
        user = self.collections[self.config.DB_USERS].find_last(
            {"_id": user_id})
        return user

    def __getitem__(self, key: str) -> Any:
        """
        Allows accessing MongoDB collections using the dot notation.
        """
        return self.collections[key]

    def __iter__(self) -> Generator[str, None, None]:
        """
        Iterator for MongoDB collections.
        """
        yield from self.collections
