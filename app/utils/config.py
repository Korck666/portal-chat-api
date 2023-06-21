# utils/config.py
from math import log
import os
from typing import Any, Optional
import logging
from dataclasses import dataclass


@dataclass
class Config:
    @staticmethod
    def log_level_dict(log_level:str="INFO") -> int:
        return {
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
            "NOTSET": logging.NOTSET
        } [log_level]


    AUTH_ALGORITHM: str = os.environ.get("AUTH_ALGORITHM", "HS256")
    LOG_LEVEL: int = log_level_dict(os.environ.get("LOG_LEVEL", "INFO"))
    DEBUG: bool = bool(os.environ.get("DEBUG", False))

    PUBLIC_URL: str = os.environ.get("PUBLIC_URL", "localhost")
    LOCAL_HOST: str = os.environ.get("HOST", "0.0.0.0")
    EXPOSED_PORT: int = int(os.environ.get("PORT", 8000))

    NGROK_TUNNEL_PORT: int = int(os.environ.get("NGROK_TUNNEL_PORT", 4040))
    NGROK_TUNNEL_URL: str = f"http://{LOCAL_HOST}:{NGROK_TUNNEL_PORT}/api/tunnels"

    LOG_FORMAT: str = os.environ.get("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    LOG_DATE_FORMAT: str = os.environ.get("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
    LOG_FILE: str = os.environ.get("LOG_FILE", "portal-chat-api.log")
    LOG_PATH: str = os.environ.get("LOG_PATH", "/var/log")
    LOG_BACKUP_PATH: str = os.environ.get("LOG_BACKUP_PATH", "/var/backup/log")
    LOG_FILE_MAX_BYTES: int = int(os.environ.get("LOG_FILE_MAX_BYTES", 1000000))
    LOG_FILE_BACKUP_COUNT: int = int(os.environ.get("LOG_FILE_BACKUP_COUNT", 10))
    PYTHONPATH: str = os.environ.get("PYTHONPATH", "/app")
    PYCACHE: str = os.environ.get("PYCACHE", "__pycache__")
    WORKDIR: str = os.environ.get("WORKDIR", "/app")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "not set")
    OPENAI_ORGANIZATION: str = os.environ.get("OPENAI_ORGANIZATION", "not set")
    API_KEY_NAME: str = os.environ.get("API_KEY_NAME", "PORTAL_CHAT_API_KEY")
    PORTAL_CHAT_API_KEY: str = os.environ.get(API_KEY_NAME, "not set")
    API_TITLE: str = os.environ.get("API_TITLE", "portal-chat-api")
    API_VERSION: str = os.environ.get("API_VERSION", "0.0.2")
    API_DESCRIPTION: str = os.environ.get("API_DESCRIPTION", "API to chat features for portal RPG game")
    CHAT_MODEL: str = os.environ.get("CHAT_MODEL", "gpt-3.5-turbo")
    FILE_CHUNCK: int = int(os.environ.get("FILE_CHUNCK", 8192))

    MONGODB_DB: str = os.environ.get("PCAPI_MONGO_DB", "portal-chat-api")
    DB_USERS: str = os.environ.get("PCAPI_MONGO_COLLECTION_USER", "users")
    DB_LOGS: str = os.environ.get("PCAPI_MONGO_COLLECTION_LOGS", "logs")
    MONGODB_URL: str = os.environ.get("PCAPI_MONGO_URL", f"mongodb://mongo:GSySaJn2JEinuRYEn9IY@containers-us-west-88.railway.app:5573")

    DISCORD_APP_AUTH_TOKEN: str = os.environ.get("DISCORD_APP_AUTH_TOKEN", "not set")
    DISCORD_APP_ID: str = os.environ.get("DISCORD_APP_ID", "not set")
    DISCORD_APP_INTENTS: int = int(os.environ.get("DISCORD_APP_INTENTS", 0))
    DISCORD_APP_PUBLIC_KEY: str = os.environ.get("DISCORD_APP_PUBLIC_KEY", "not set")
    DISCORD_BOT_APP_INVITE_LINK: str = os.environ.get("DISCORD_BOT_APP_INVITE_LINK", "not set")

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
