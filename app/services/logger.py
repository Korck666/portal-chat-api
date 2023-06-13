from collections.abc import Iterable
import logging
from typing import Optional

from services.mongodb_handler import MongoDBHandler
from services.mongodb import MongoDB
import utils.config as config


class Logger():
    """
    Singleton class to handle logging.

    Args:
    None

    Returns:
    logging.Logger: The instantiated logger object.
    """

    _instance: Optional['Logger'] = None

    def __new__(cls) -> logging.Logger:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.logger = logging.getLogger()
            cls.config = config.Config()
            cls.mongodb = MongoDB()
            cls.logger.setLevel(cls.config.LOG_LEVEL)
            cls.dbhandler = MongoDBHandler(
                collection=cls.mongodb.collections[cls.config.DB_LOGS])
            cls.dbhandler.setFormatter(
                logging.Formatter(cls.config.LOG_FORMAT))
            cls.logger.addHandler(cls.dbhandler)
            cls.new_filehandler()
        return cls.logger

    @classmethod
    def new_filehandler(cls) -> None:
        cls.filehandler = logging.FileHandler(
            f"{cls.config.LOG_PATH}/{cls.config.LOG_FILE}")
        cls.filehandler.setFormatter(
            logging.Formatter(cls.config.LOG_FORMAT))
        cls.logger.addHandler(cls.filehandler)
        cls.logger.info("New log file.")

    def __init__(self) -> None:
        pass
