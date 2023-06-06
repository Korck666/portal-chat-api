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

MONGO_CHAT_API_SETTINGS = dict(json.loads(
    get_env_variable("MONGO_CHAT_API_SETTINGS")))
print("=====================================")
print("MONGO_CHAT_API_SETTINGS")
print("=====================================")
for k, v in MONGO_CHAT_API_SETTINGS.items():
    print(f"{k}:{v}")
print("=====================================")
MDB_USERS = MONGO_CHAT_API_SETTINGS["MDB_USERS_COLLECTION"]
MDB_LOGS = MONGO_CHAT_API_SETTINGS["MDB_LOGS_COLLECTION"]
MDB_DATABASE = MONGO_CHAT_API_SETTINGS["MDB_DATABASE"]
MONGO_URL = get_env_variable("MONGO_URL")
