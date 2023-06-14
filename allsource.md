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
│   │   ├── 2304.03442.pdf
│   │   └── coding_project_python.pdf
│   └── utils
│       ├── __init__.py
│       ├── cleanup.py
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

11 directories, 41 files
```

```python
# Content of ./app/main.py:
# main.py: This file sets up the FastAPI application and includes the routers.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from routers import file_man, chat, keepalive, healthcheck
import os
from utils.config import Config
from services.logger import Logger

logger = Logger()
config = Config()

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
from pydantic import config
from services.auth import Authenticator
from utils.config import Config
from models.chat_input import ChatInput
from models.chat_output import ChatOutput
from services.openai import OpenAI

router = APIRouter()
chat_model = OpenAI()
config = Config()
auth = Authenticator("api_key")
# TODO: Add config for chat prompts and responses with langchain
chat_prep = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."""


@router.post("/chat", response_model=ChatOutput, dependencies=[Depends(auth.auth_header_dependency)])
def chat_endpoint(chat_input: ChatInput):
    # we may do some preprocessing here
    # Return the response
    return ChatOutput(response=chat_model.chat(config.CHAT_MODEL, chat_prep, chat_input.message))

# Content of ./app/routers/file_man.py:
# routers/file_man.py
import asyncio
from logging import Logger, raiseExceptions
from fastapi import APIRouter, status
from pydantic import config
from utils.config import Config
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi import UploadFile, HTTPException
from typing import List
import os
from services.logger import Logger

router = APIRouter()
logger = Logger()
config = Config()

router.mount(f"{config.WORKDIR}/upload",
             StaticFiles(directory="upload"), name="upload")


async def save_file(file: UploadFile):
    try:
        # TODO: Add a better check for file type
        file_name: str = file.filename if file.filename is not None else ""
        if file_name.endswith('.pdf'):
            with open(f"{config.WORKDIR}/upload/{file.filename}", "wb") as buffer:
                while True:
                    chunk = await file.read(config.FILE_CHUNCK)
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
from models.token_data import TokenData
from services.auth import Authenticator
from services.healthcheck import HealthCheck

router = APIRouter()

auth = Authenticator("api_key")


@router.get("/healthcheck", dependencies=[Depends(auth.auth_header_dependency)])
async def healthcheck() -> JSONResponse:
    # we may do some preprocessing here
    auth_token = TokenData(scopes=["healthcheck"])
    try:
        checks = await HealthCheck.healthcheck(auth_token)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

    # Return the response
    return JSONResponse(status_code=200, content={"message": checks})

# Content of ./app/routers/keepalive.py:
# routers/keepalive.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services.auth import Authenticator
from services.keepalive import KeepAlive
from models.token_data import TokenData

router = APIRouter()

auth = Authenticator("api_key")


@router.get("/keepalive", dependencies=[Depends(auth.auth_header_dependency)])
def keepalive() -> JSONResponse:
    # we may do some preprocessing here
    auth_token = TokenData(scopes=["keepalive"])
    # Return the response
    return KeepAlive.keepalive(auth_token)

# Content of ./app/routers/__init__.py:


# Content of ./app/services/auth.py:
import asyncio
from ctypes import Union
from typing import Callable, Dict
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from utils.config import Config
from models.token_data import TokenData
from services.mongodb import MongoDB
from services.logger import Logger


class Authenticator:
    def __init__(self, auth_type: str):
        self.auth_type = auth_type
        self.config = Config()
        self.mongodb = MongoDB()
        self.logger = Logger()

        if self.auth_type == "api_key":
            self.auth_header = APIKeyHeader(
                name=self.config.API_KEY_NAME, auto_error=False)
            self.authenticate = self.authenticate_api_key
        elif self.auth_type == "oauth2":
            self.auth_scheme = OAuth2PasswordBearer(
                tokenUrl=self.config.API_KEY_NAME, auto_error=False)
            self.authenticate = self.authenticate_user
        else:
            raise ValueError(
                "Invalid authentication type specified. Valid options are 'api_key' or 'oauth2'.")

    @property
    def auth_header_dependency(self) -> Callable:
        return lambda: Depends(self.auth_header)

    @property
    def auth_scheme_dependency(self) -> Callable:
        return lambda: Depends(self.auth_scheme)

    async def authenticate_api_key(self) -> str | None:
        api_key_header = await self.auth_header_dependency()
        if api_key_header != self.config.PORTAL_CHAT_API_KEY:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Incorrect API key",
                                headers={"WWW-Authenticate": "Bearer"})
        return api_key_header

    async def authenticate_user(self) -> Dict | None:
        token = await self.auth_scheme_dependency()
        try:
            payload = jwt.decode(token, self.config.PORTAL_CHAT_API_KEY,
                                 algorithms=[self.config.AUTH_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                self.logger.error("Could not validate credentials")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Could not validate credentials",
                                    headers={"WWW-Authenticate": "Bearer"})
            token_data = TokenData(username=username)
        except PyJWTError:
            self.logger.error("Could not validate credentials")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"})
        loop = asyncio.get_event_loop()
        user_data = await loop.run_in_executor(None, self.mongodb.get_user, token_data.username)
        if user_data is None:
            self.logger.error("Could not find user data")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"})
        return user_data

# Content of ./app/services/healthcheck.py:
import asyncio
import time

from typing import List, Optional
from routers.file_man import JSONResponse
from models.token_data import TokenData
from services.logger import Logger

logger = Logger()


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

    def __init__(self, service_name: Optional[str] = None):
        self.service_name = service_name or __name__
        self._instances.append(self)

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
            response: Optional[JSONResponse] = await task
            end_time = time.time()
            response_time = end_time - start_time
            if response is not None:
                responses.append(JSONResponse(status_code=200, content={
                    "message": response.body[slice("message", "message" + "\0")], "response_time": response_time}))
        return responses

# Content of ./app/services/keepalive.py:
# services/keepalive.py

import asyncio
from models.token_data import TokenData
from routers.file_man import JSONResponse
from typing import List, Optional
from services.logger import Logger

logger = Logger()


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
    async def _run_keepalive(cls, instance, auth_token):
        try:
            await instance._keepalive(auth_token)
        except Exception as e:
            logger.error(f"{instance.service_name} | keepalive - ERROR: {e}")

    @classmethod
    def keepalive(cls, auth_token: Optional[TokenData]) -> JSONResponse:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            tasks = [cls._run_keepalive(instance, auth_token)
                     for instance in cls._instances]
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()
        return JSONResponse(status_code=200, content={"message": "OK"})

# Content of ./app/services/logger.py:
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

# Content of ./app/services/mongodb.py:
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
from typing import Any

import openai
from utils.config import Config


class OpenAI():
    """
    Singleton class for interacting with the OpenAI API.
    """
    _instance = None

    def __new__(cls) -> "OpenAI":
        """
        Singleton implementation for class OpenAI.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """
        Initializes OpenAI connection and collections.
        """
        self.config = Config()
        openai.api_key = self.config.OPENAI_API_KEY
        openai.organization = self.config.OPENAI_ORGANIZATION

    def chat(self, chat_model: str, chat_prep: str, chat_message: str) -> str:
        """
        Calls the OpenAI API to generate a response based on a given model, preparation, and message.

        Args:
            chat_model (str): The OpenAI model to use for generating the response.
            chat_prep (str): The preparation message to send to OpenAI.
            chat_message (str): The user message to send to OpenAI.

        Returns:
            str: The response generated by OpenAI.
        """
        response: Any = openai.ChatCompletion.create(
            model=chat_model,
            messages=[
                {"role": "system", "content": chat_prep},
                {"role": "user", "content": chat_message},
            ]
        )
        response_message: str = response["choices"][0]["message"]["content"]

        return response_message

# Content of ./app/services/__init__.py:

# Content of ./app/utils/cleanup.py:
# util/cleanup.py
import shutil
from typing import Optional
from pathlib import Path
from threading import Lock
import logging
import utils.config as config
from services.logger import Logger
import datetime
import os

logger = Logger()


class Cleanup:
    """
    Singleton class to handle cleanup operations
    """
    __instance = None

    def __new__(cls) -> "Cleanup":
        """
        Create a new instance of the class if it doesn't exist
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self) -> None:
        """
        Initialize the cleanup instance
        """
        if self.__initialized:
            return
        self.__initialized = True
        self.lock = Lock()
        self.config = config.Config()
        self.PYCACHE = self.config.PYCACHE
        self.root_dir = Path(self.config.WORKDIR)

    def cleanup_cache(self, root_dir: Optional[str] = None) -> None:
        """
        Recursively deletes cache folders from the specified directory or the root directory
        :param root_dir: directory to delete from
        :type root_dir: str
        """
        root: Path = Path(root_dir) if root_dir is not None else self.root_dir
        for path in root.glob('**/*'):
            if path.is_dir() and path.name == self.PYCACHE:
                logger.info(f"Deleting cache folder: {path}")
                shutil.rmtree(path)
            elif path.is_dir() and path.name.startswith('.'):
                logger.debug(f"Skipping hidden folder: {path}")

    def check_log_size(self) -> None:
        """
        Checks the size of the current log file
        """
        # check log file size and backup rules here
        logger.info("Checking log file size.")
        # check log file size and backup rules here
        if self.config.LOG_FILE_MAX_BYTES*0.99 >= Logger.filehandler.stream.tell():
            logger.warning("Log file has reached the maximum size.")
            self.close_log_file()

        logger.info("Deleting extra backup log files.")
        # delete any extra backup log files beyond the specified backup rules

    def close_log_file(self) -> None:
        """
        Closes the current log file
        """
        logger.info("Closing the current log file.")
        with self.lock:
            # when closing the log file, close the handler and open a new one
            Logger.filehandler.flush()
            Logger.filehandler.close()
            logger.removeHandler(Logger.filehandler)
            # move the log file to the backup location
            self.move_to_backup()
            Logger.new_filehandler()

    def move_to_backup(self) -> None:
        """
        Moves the current log file to backup
        """
        logger.info("Checking backup rules.")
        # TODO: check the number of backup files and delete any extra backup files

        if not os.path.exists(self.config.LOG_BACKUP_PATH):
            os.mkdir(self.config.LOG_BACKUP_PATH)
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            backup_filename = f"{timestamp}_{self.config.LOG_FILE}"
            fromlog = f"{self.config.LOG_PATH}/{self.config.LOG_FILE}"
            tobackup = f"{self.config.LOG_BACKUP_PATH}/{backup_filename}"
            shutil.copy(fromlog, tobackup)
            logger.info(f"Moved closed log file to backup {backup_filename}")

# Content of ./app/utils/config.py:
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

# Content of ./app/utils/__init__.py:


```
