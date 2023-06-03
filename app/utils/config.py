# utils/config.py
import os


def get_env_variable(variable_name: str) -> str:
    value = os.getenv(variable_name)
    if value is None:
        raise Exception(f"Environment variable {variable_name} is not set.")
    return value


WORKDIR = get_env_variable("PWD")
OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")
OPENAI_ORGANIZATION = get_env_variable("OPENAI_ORG_ID")


API_TITLE = "PDF to Text API"
API_VERSION = "0.1.0"
API_DESCRIPTION = "API to convert PDFs to text"

CHAT_MODEL = "gpt-3.5-turbo"  # the default chat model

FILE_CHUNCK: int = [1024,  # 1KB read/write chunck size for file operations
                    2048,  # 2KB read/write chunck size for file operations
                    4096,  # 4KB read/write chunck size for file operations
                    8192,  # 8KB read/write chunck size for file operations
                    16384,  # 16KB read/write chunck size for file operations
                    32768]  # 32KB read/write chunck size for file operations
DEFAULT_FILE_CHUNCK_INDEX: int = 3  # 8192 bytes
