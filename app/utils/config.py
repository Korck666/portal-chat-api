# utils/config.py
import os
from typing import Any, Optional


class Config:
    _instance: Optional["Config"] = None
    _cache = {}

    def __new__(cls) -> "Config":
        """
        Get singleton instance of Config

        Returns:
        Config: Singleton instance of Config
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize Config class.

        Returns:
        None
        """
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.AUTH_ALGORITHM = "HS256"  # set authentication algorithm
            self.LOG_LEVEL: str = self.get_env_variable(
                "LOG_LEVEL", default="INFO")  # set logging level
            self.DEBUG: bool = bool(self.get_env_variable(
                "DEBUG", default=False))  # set DEBUG flag
            self.HOST: str = self.get_env_variable(
                "HOST", default="0.0.0.0")  # set HOST IP address
            self.PORT: int = int(self.get_env_variable(
                "PORT", default=8000))  # set PORT number
            self.LOG_LEVEL: str = self.get_env_variable(
                "LOG_LEVEL", default="INFO")  # set logging level
            self.LOG_FORMAT: str = self.get_env_variable(
                "LOG_FORMAT", default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")  # set logging format
            self.LOG_DATE_FORMAT: str = self.get_env_variable(
                "LOG_DATE_FORMAT", default="%Y-%m-%d %H:%M:%S")  # set logging date format
            self.LOG_FILE: str = self.get_env_variable(
                "LOG_FILE", default="portal-chat-api.log")  # set logging file name
            self.LOG_PATH: str = self.get_env_variable(
                "LOG_PATH", default="/var/log")  # set logging file path
            self.LOG_BACKUP_PATH: str = self.get_env_variable(
                "LOG_BACKUP_PATH", default="/var/backup/log")  # set logging file path
            self.LOG_FILE_MAX_BYTES: int = int(self.get_env_variable(
                "LOG_FILE_MAX_BYTES", default=1000000))  # set max size for log file
            self.LOG_FILE_BACKUP_COUNT: int = int(self.get_env_variable(
                "LOG_FILE_BACKUP_COUNT", default=10))  # set number of backup log files to keep
            self.PYTHONPATH: str = self.get_env_variable(
                "PYTHONPATH", default="/app")  # set PYTHONPATH
            self.PYCACHE: str = self.get_env_variable(
                "PYCACHE", default="__pycache__")  # set pycache directory name
            self.WORKDIR: str = self.get_env_variable(
                "PWD", default="/app")  # set working directory
            self.OPENAI_API_KEY: str = self.get_env_variable(
                "OPENAI_API_KEY", default="not set")  # set OpenAI API key
            self.OPENAI_ORGANIZATION: str = self.get_env_variable(
                "OPENAI_ORG_ID", default="not set")  # set OpenAI organization
            self.API_KEY_NAME: str = "PORTAL_CHAT_API_KEY"
            self.PORTAL_CHAT_API_KEY: str = self.get_env_variable(
                self.API_KEY_NAME, default="not set")
            self.API_TITLE: str = "portal-chat-api"
            self.API_VERSION: str = "0.0.2"
            self.API_DESCRIPTION: str = "API to chat features for portal RPG game"
            self.CHAT_MODEL: str = "gpt-3.5-turbo"  # the default chat model
            # read/write chunck sizes for file operations
            self.FILE_CHUNCK: int = 8192
            # MongoDB connection
            self.MONGODB_HOST: str = self.get_env_variable(
                "MONGODB_HOST", default="localhost")
            self.MONGODB_PORT: int = int(self.get_env_variable(
                "MONGODB_PORT", default=27017))
            self.MONGODB_DB: str = self.get_env_variable(
                "PCAPI_MONGO_DB", default="portal-chat-api")
            self.DB_USERS: str = self.get_env_variable(
                "PCAPI_MONGO_COLLECTION_USER", default="users")
            self.DB_LOGS: str = self.get_env_variable(
                "PCAPI_MONGO_COLLECTION_LOGS", default="logs")
            self.MONGODB_URL: str = self.get_env_variable(
                "PCAPI_MONGO_URL", default=f"mongodb://{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_DB}")

    def get_env_variable(self, name: str, default: Optional[Any] = None) -> Any:
        """
        Get environment variable value.

        Args:
        - name (str): Name of the environment variable.
        - default (Optional[Any]): Default value to return if environment variable is not set.

        Returns:
        - Any: Value of the environment variable or default value if environment variable is not set.
        """
        value = os.environ.get(name)
        if value is None:
            if default is not None:
                return default
            raise ValueError(f"Environment variable {name} is not set.")
        return value
