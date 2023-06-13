# Directory Structure

```text
.
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── chat_input.py
│   │   ├── chat_output.py
│   │   └── token_data.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── file_man.py
│   │   ├── healthcheck.py
│   │   └── keepalive.py
│   ├── scripts
│   │   ├── postcommand.sh
│   │   ├── print_source.sh
│   │   └── run_portal_api.sh
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── healthcheck.py
│   │   ├── keepalive.py
│   │   ├── logger.py
│   │   ├── mongodb.py
│   │   ├── mongodb_handler.py
│   │   └── openai.py
│   ├── static
│   │   ├── favincon16.png.png
│   │   ├── favincon32.png.png
│   │   └── logo_rpg_portal.png
│   ├── upload
│   └── utils
│       ├── __init__.py
│       └── config.py
├── compose-dev.yaml
├── requirements.txt
├── templates
│   ├── game_payload
│   │   ├── worldCreation.json
│   │   └── worldCreationExample.json
│   └── game_systems
│       ├── DnD 5e Players Handbook (BnW OCR)-Fixed Pages.pdf
│       ├── GURPS - 4th Edition - Basic Set.pdf
│       ├── Pathfinder_Core_Rulebook.pdf
│       └── cyberpunk.pdf
└── tree.md

11 directories, 38 files
```

```python
# Content of ./app/main.py:
# main.py: This file sets up the FastAPI application and includes the routers.

from utils import config
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from services.logger import logger
from routers import file_man, chat, keepalive, healthcheck
from logging import log
import os

# Clean up cache
os.system("rm -rf app/__pycache__")

logger.info("Starting app...")

# Initialize the FastAPI application
app = FastAPI(docs_url=None, redoc_url=None,
              title=config.API_TITLE,
              version=config.API_VERSION,
              description=config.API_DESCRIPTION,
              )

logger.info("FastAPI application setup successful.")

# Mount static files
try:
    logger.info("Adding static files...")
    app.mount(f"{config.WORKDIR}/static",
              StaticFiles(directory="static"), name="static")
    logger.info("Static files added successfully.")
except Exception as e:
    logger.error(f"Error adding static files: {e}")

# Add routers
try:
    logger.info("Adding routers...")
    app.include_router(file_man.router)
    app.include_router(chat.router)
    app.include_router(keepalive.router)
    app.include_router(healthcheck.router)
    logger.info("Routers added successfully.")
except Exception as e:
    logger.error(f"Error adding routers: {e}")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html(req: Request) -> HTMLResponse:
    """Returns the Swagger UI HTML for API documentation."""
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = f"{root_path}{app.openapi_url}"
    oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url
    if oauth2_redirect_url:
        oauth2_redirect_url = f"{root_path}{oauth2_redirect_url}"
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=f"{app.title}   - Swagger UI",
        oauth2_redirect_url=oauth2_redirect_url,
        init_oauth=app.swagger_ui_init_oauth,
        swagger_favicon_url="/static/favicon32.png",
        swagger_ui_parameters=app.swagger_ui_parameters,
    )


@app.get("/")
def home() -> RedirectResponse:
    """Redirects to the docs page."""
    return RedirectResponse("/docs")

# Content of ./app/models/chat_input.py:
# models/chat_input.py
from pydantic import BaseModel


class ChatInput(BaseModel):
    message: str

# Content of ./app/models/chat_output.py:
# models/chat_output.py
from pydantic import BaseModel


class ChatOutput(BaseModel):
    response: str

# Content of ./app/models/token_data.py:
# model/token_data.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []
    expires_at: Optional[datetime] = None

# Content of ./app/models/__init__.py:

# Content of ./app/routers/chat.py:
# routers/chat.py
from fastapi import APIRouter, Depends
from services.auth import authenticate_api_key
from utils import config
from models.chat_input import ChatInput
from models.chat_output import ChatOutput
from services import openai

router = APIRouter()

# TODO: Add config for chat prompts and responses with langchain
chat_prep = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."""


@router.post("/chat", response_model=ChatOutput, dependencies=[Depends(authenticate_api_key)])
def chat_endpoint(chat_input: ChatInput):
    # we may do some preprocessing here
    # Return the response
    return ChatOutput(response=openai.chat(config.CHAT_MODEL, chat_prep, chat_input.message))

# Content of ./app/routers/file_man.py:
# routers/file_man.py
import asyncio
from logging import Logger, raiseExceptions
from fastapi import APIRouter, status
from utils import config
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi import UploadFile, HTTPException
from typing import List
import os
from utils import config
from services.logger import logger

router = APIRouter()

router.mount(f"{config.WORKDIR}/upload",
             StaticFiles(directory="upload"), name="upload")


async def save_file(file: UploadFile):
    try:
        # TODO: Add a better check for file type
        file_name: str = file.filename if file.filename is not None else ""
        if file_name.endswith('.pdf'):
            with open(f"{config.WORKDIR}/upload/{file.filename}", "wb") as buffer:
                while True:
                    chunk = await file.read(config.FILE_CHUNCK[config.DEFAULT_FILE_CHUNCK_INDEX])
                    if not chunk:  # End of file
                        break
                    buffer.write(chunk)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Only PDFs are accepted.")
    except IOError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/list_pdfs/")
def list_files():
    files = os.listdir(f"{config.WORKDIR}/upload")
    return JSONResponse(status_code=200, content={"files": files})


@router.get("/download_pdfs/{file_name}")
async def download_file(file_name: str):
    path = f"{config.WORKDIR}/upload/"
    if os.path.exists(f"{path}{file_name}"):
        return FileResponse(path=f"{path}{file_name}",
                            status_code=200,
                            filename=file_name,
                            media_type="application/pdf",
                            content_disposition_type="attachment")
    raise HTTPException(status_code=404, detail="File not found.")


@router.post("/upload_pdfs/")
async def upload_files(files: List[UploadFile] = []):
    tasks = []
    for file in files:
        tasks.append(asyncio.ensure_future(save_file(file)))
    await asyncio.gather(*tasks)
    return JSONResponse(status_code=200, content={"message": "Files uploaded successfully."})

# Content of ./app/routers/healthcheck.py:
# routers/healtcheck.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services import auth
from services.auth import authenticate_api_key
from services.healthcheck import HealthCheck

router = APIRouter()


@router.get("/healthcheck", dependencies=[Depends(authenticate_api_key)])
def healthcheck() -> JSONResponse:
    # we may do some preprocessing here
    auth_token = auth.TokenData(scopes=["healthcheck"])
    # Return the response
    return HealthCheck.healthcheck(auth_token)

# Content of ./app/routers/keepalive.py:
# routers/keepalive.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services import auth
from services.auth import authenticate_api_key
from services.keepalive import KeepAlive

router = APIRouter()


@router.get("/keepalive", dependencies=[Depends(authenticate_api_key)])
def keepalive() -> JSONResponse:
    # we may do some preprocessing here
    auth_token = auth.TokenData(scopes=["keepalive"])
    # Return the response
    return KeepAlive.keepalive(auth_token)

# Content of ./app/routers/__init__.py:

# Content of ./app/services/auth.py:
# routers/auth.py
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
import services.mongodb as mongodb
from utils.config import (API_KEY_NAME, PORTAL_CHAT_API_KEY, AUTH_ALGORITHM)
import jwt
from jwt import PyJWTError
from models.token_data import TokenData
from services.logger import logger

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def authenticate_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != PORTAL_CHAT_API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Incorrect API key",
                            headers={"WWW-Authenticate": "Bearer"})
    return api_key_header


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=API_KEY_NAME)


async def authenticate_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, PORTAL_CHAT_API_KEY,
                             algorithms=[AUTH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            # TODO: Add logging and extra info to from the exception
            logger.error("Could not validate credentials")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(username=username)
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    user = mongodb.get_user(username=token_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user

# Content of ./app/services/healthcheck.py:
# services/keepalive.py

import asyncio
import time
from models.token_data import TokenData
from routers.file_man import JSONResponse
from services.logger import logger
from typing import List, Optional


class HealthCheck:
    """
    A class used to represent the HealthCheck service

    ...

    Attributes
    ----------
    _instances : list
        a class variable to keep track of all instances of this class

    Methods
    -------
    _healthcheck():
        The default implementation of the healthcheck method. Can be overridden in subclasses.
    healthcheck():
        Class method that calls the _healthcheck method on all instances of this class and measures the response time.
    """

    _instances: List['HealthCheck'] = []

    def __init__(self, service_name: Optional[str]):
        self._instances.append(self)
        # add the service name to the logger
        self.service_name = service_name or __name__

    async def _healthcheck(self, auth_token: Optional[TokenData]) -> JSONResponse:
        # Default implementation adds a log message with the service name
        message = f"{self.service_name} | healthcheck - OK"
        logger.info(message)
        return JSONResponse(status_code=200, content={"message": message})

    @classmethod
    async def healthcheck(cls, auth_token: Optional[TokenData]) -> List[JSONResponse]:
        # Use asyncio.gather to run all _healthcheck checks concurrently
        tasks = [instance._healthcheck(auth_token)
                 for instance in cls._instances]
        responses = []
        for task in asyncio.as_completed(tasks):
            start_time = time.time()
            response = await task
            end_time = time.time()
            response_time = end_time - start_time
            responses.append(JSONResponse(status_code=200, content={
                             "message": response.json().get("message"), "response_time": response_time}))
        return responses

# Content of ./app/services/keepalive.py:
# services/keepalive.py

import asyncio
from models.token_data import TokenData
from routers.file_man import JSONResponse
from services.logger import logger
from typing import List, Optional


class KeepAlive:
    """
    A class used to represent the KeepAlive service

    ...

    Attributes
    ----------
    _instances : list
        a class variable to keep track of all instances of this class

    Methods
    -------
    _keepalive():
        The default implementation of the keepalive check. Can be overridden in subclasses.
    keepalive():
        Class method that calls the _keepalive method on all instances of this class.
    """

    _instances: List['KeepAlive'] = []

    def __init__(self, service_name: Optional[str]):
        self._instances.append(self)
        # add the service name to the logger
        self.service_name = service_name or __name__

    async def _keepalive(self, auth_token: Optional[TokenData]) -> JSONResponse:
        # Default implementation adds a log message with the service name
        message = f"{self.service_name} | keepalive - OK"
        logger.info(message)
        return JSONResponse(status_code=200, content={"message": message})

    @classmethod
    def keepalive(cls, auth_token: Optional[TokenData]) -> JSONResponse:
        # Use asyncio.gather to run all _keepalive checks concurrently
        asyncio.gather(*(instance._keepalive(auth_token)
                         for instance in cls._instances))
        return JSONResponse(status_code=200, content={"message": "OK"})

# Content of ./app/services/logger.py:
import logging
from services.mongodb_handler import MongoDBHandler
from services.mongodb import collections, MDB_LOGS

logger = logging.getLogger(__name__)

# TODO: set level from startup config
logger.setLevel(logging.INFO)

handler = MongoDBHandler(collection=collections[MDB_LOGS])

# handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(handler)

# Content of ./app/services/mongodb.py:
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


def get_user(username: str | None) -> Any:
    user = collections[MDB_USERS].find_one({"username": username})
    return user

# Content of ./app/services/mongodb_handler.py:
# service/mongodb_handler.py
import logging

class MongoDBHandler(logging.Handler):
    def __init__(self, collection):
        logging.Handler.__init__(self)
        self.collection = collection

    def emit(self, record):
        # Insert a new document into the collection with the log record's attributes
        self.collection.insert_one(record.__dict__)


# Content of ./app/services/openai.py:
# services/openai.py
from typing import Any, Generator
import openai
from utils import config

openai.api_key = config.OPENAI_API_KEY
openai.organization = config.OPENAI_ORGANIZATION


def chat(chat_model: str, chat_prep: str, chat_message: str) -> str:
    # Call OpenAI API
    openai_response: Any = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": chat_prep},
            {"role": "user", "content": chat_message},
        ]
    )

    response_message: Any = openai_response["choices"]
    response_message: Any = response_message[0]
    response_message: Any = response_message["message"]
    response_message: Any = response_message["content"]

    return response_message

# Content of ./app/services/__init__.py:
class services:
    """
    A module used to represent the services package

    ...

    Attributes
    ----------
    __all__ : list
        a list of all modules in the package

    Methods
    -------
    """
    __all__: list[str] = ['auth', 'healthcheck',
                          'keepalive', 'mongodb',
                          'openai', 'logger']

    @classmethod
    def services(cls) -> list[str]:
        return cls.__all__

# Content of ./app/utils/config.py:
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

# Content of ./app/utils/__init__.py:

```
