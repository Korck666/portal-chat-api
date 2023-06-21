# app/services/logger.py

import logging

from typing import Optional
from utils.config import Config
from services.mongodb import MongoDB
from services.mongodb_handler import MongoDBHandler


class Logger(logging.Logger):
    """
    Singleton class to handle logging.
    """
    logger: Optional['Logger'] = None
    config = Config()
    mongodb = MongoDB()

    def __new__(cls) -> 'Logger':
        if cls.logger is None:
            cls.logger = super().__new__(cls)
            cls.logger.__init__()
        return cls.logger

    def __init__(self, name: str="System", level: int=config.LOG_LEVEL) -> None:
        super().__init__(name, level)
        self.dbhandler = MongoDBHandler(
            collection=self.mongodb.collections[self.config.DB_LOGS])
        self.dbhandler.setFormatter(
            logging.Formatter(self.config.LOG_FORMAT))
        self.addHandler(self.dbhandler)
        self.new_filehandler()

    @classmethod
    def new_filehandler(cls) -> None:
        cls.config = Config()
        cls.filehandler = logging.FileHandler(
            f"{cls.config.LOG_PATH}/{cls.config.LOG_FILE}")
        cls.filehandler.setFormatter(
            logging.Formatter(cls.config.LOG_FORMAT))
        cls.logger.addHandler(cls.filehandler) if cls.logger else None
        cls.logger.info("New log file.") if cls.logger else None
