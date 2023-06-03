# utils/config.py
import os
from typing import List


def get_env_variable(variable_name: str) -> str:
    value = os.getenv(variable_name)
    if value is None:
        raise Exception(f"Environment variable {variable_name} is not set.")
    return value


WORKDIR = get_env_variable("PWD")

OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")
OPENAI_ORGANIZATION = get_env_variable("OPENAI_ORG_ID")

API_KEY_NAME = "PORTAL_CHAT_API_KEY"
PORTAL_CHAT_API_KEY = get_env_variable(API_KEY_NAME)


API_TITLE = "PDF to Text API"
API_VERSION = "0.1.0"
API_DESCRIPTION = "API to convert PDFs to text"

CHAT_MODEL = "gpt-3.5-turbo"  # the default chat model

FILE_CHUNCK: list[int] = [1024,  # 1KB read/write chunck size for file operations
                          2048,  # 2KB read/write chunck size for file operations
                          4096,  # 4KB read/write chunck size for file operations
                          8192,  # 8KB read/write chunck size for file operations
                          16384,  # 16KB read/write chunck size for file operations
                          32768]  # 32KB read/write chunck size for file operations
DEFAULT_FILE_CHUNCK_INDEX: int = 3  # 8192 bytes

AUTH_ALGORITHM: str = "HS256"

# MongoDB
#'{"MDB_DATABASE":"portal-chat-api", "MDB_USERS_COLLECTION":"users", "MDB_LOGS_COLLECTION":"logs"}'
MONGO_CHAT_API_SETTINGS=eval(get_env_variable("MONGO_CHAT_API_SETTINGS"))
MDB_USERS = MONGO_CHAT_API_SETTINGS["MDB_USERS_COLLECTION"]
MDB_LOGS = MONGO_CHAT_API_SETTINGS["MDB_LOGS_COLLECTION"]
MDB_DATABASE = MONGO_CHAT_API_SETTINGS["MDB_DATABASE"]
MONGO_URL = get_env_variable("MONGO_URL")