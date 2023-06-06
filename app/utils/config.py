# utils/config.py
import os
from typing import List

import json


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


API_TITLE = "portal-chat-api"
API_VERSION = "0.0.2"
API_DESCRIPTION = "API to chat features for portal RPG game"

CHAT_MODEL = "gpt-3.5-turbo"  # the default chat model

FILE_CHUNCK: list[int] = [1024,  # 1KB read/write chunck size for file operations
                          2048,  # 2KB read/write chunck size for file operations
                          4096,  # 4KB read/write chunck size for file operations
                          8192,  # 8KB read/write chunck size for file operations
                          16384,  # 16KB read/write chunck size for file operations
                          32768]  # 32KB read/write chunck size for file operations
DEFAULT_FILE_CHUNCK_INDEX: int = 3  # 8192 bytes

AUTH_ALGORITHM: str = "HS256"

print("=====================================")
print("MONGO_CHAT_API_SETTINGS")
print("=====================================")
MONGO_URL = get_env_variable("PCAPI_MONGO_URL")
print(f"MONOGO_URL: {MONGO_URL}")
MDB_DATABASE = get_env_variable("PCAPI_MONGO_DB")
print(f"MDB_DATABASE: {MDB_DATABASE}")
MDB_USERS = get_env_variable("PCAPI_MONGO_COLLECTION_USER")
print(f"MDB_USERS: {MDB_USERS}")
MDB_LOGS = get_env_variable("PCAPI_MONGO_COLLECTION_LOGS")
print(f"MDB_LOGS: {MDB_LOGS}")
print("=====================================")
