# Directory Structure

```text
.
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── main.py
│   ├── models
│   │   ├── ChatInput.py
│   │   ├── ChatOutput.py
│   │   └── __init__.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── file_man.py
│   ├── scripts
│   │   ├── postcommand.sh
│   │   ├── print_source.sh
│   │   └── run_portal_api.sh
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── openai.py
│   ├── static
│   │   ├── favincon16.png.png
│   │   ├── favincon32.png.png
│   │   └── logo_rpg_portal.png
│   ├── upload
│   │   ├── DnD 5e Players Handbook (BnW OCR)-Fixed Pages.pdf
│   │   ├── GURPS - 4th Edition - Basic Set.pdf
│   │   ├── Pathfinder_Core_Rulebook.pdf
│   │   └── cyberpunk.pdf
│   └── utils
│       ├── __init__.py
│       └── config.py
├── compose-dev.yaml
├── directory-tree.md
├── requirements.txt
└── templates
    ├── worldCreation.json
    └── worldCreationExample.json

9 directories, 30 files
```

```python
# Content of ./app/main.py:
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from fastapi import FastAPI
from utils import config
from routers import file_man, chat

app = FastAPI(docs_url=None, redoc_url=None,
              title=config.API_TITLE,
              version=config.API_VERSION,
              description=config.API_DESCRIPTION,
              )

app.mount(f"{config.WORKDIR}/static",
          StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html(req: Request) -> HTMLResponse:
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = f"{root_path}{app.openapi_url}"
    oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url
    if oauth2_redirect_url:
        oauth2_redirect_url = f"{root_path}{oauth2_redirect_url}"
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=f"{app.title} +  - Swagger UI",
        oauth2_redirect_url=oauth2_redirect_url,
        init_oauth=app.swagger_ui_init_oauth,
        swagger_favicon_url="/static/favicon32.png",
        swagger_ui_parameters=app.swagger_ui_parameters,
    )


@app.get("/")
def home():
    return RedirectResponse("/docs")


# add routers
app.include_router(file_man.router)
app.include_router(chat.router)

# Content of ./app/models/ChatInput.py:
# models/ChatInput.py
from pydantic import BaseModel


class ChatInput(BaseModel):
    message: str

# Content of ./app/models/ChatOutput.py:
# models/ChatOutput.py
from pydantic import BaseModel


class ChatOutput(BaseModel):
    response: str

# Content of ./app/models/__init__.py:

# Content of ./app/routers/chat.py:
# routers/chat.py
from fastapi import APIRouter
from utils import config
from models.ChatInput import ChatInput
from models.ChatOutput import ChatOutput
from services import openai

router = APIRouter()

# TODO: Add config for chat prompts and responses with langchain
chat_prep = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."""


@router.post("/chat", response_model=ChatOutput)
def chat_endpoint(chat_input: ChatInput):
    # Return the response
    return ChatOutput(response=openai.chat(config.CHAT_MODEL, chat_prep, chat_input.message))

# Content of ./app/routers/file_man.py:
# routers/file_man.py
import asyncio
from fastapi import APIRouter
from utils import config
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi import UploadFile, HTTPException
from typing import List
import os
from utils import config

router = APIRouter()

router.mount(f"{config.WORKDIR}/upload",
             StaticFiles(directory="upload"), name="upload")


async def save_file(file: UploadFile):
    if file.filename.endswith('.pdf'):
        with open(f"{config.WORKDIR}/upload/{file.filename}", "wb") as buffer:
            while True:
                # TODO: Add error handling, if chunk is too big, we can ajust the chunk size dinamically
                # TODO: Add a progress bar
                # TODO: Add error recovery retries
                chunk = await file.read(config.FILE_CHUNCK[config.DEFAULT_FILE_CHUNCK_INDEX])
                if not chunk:  # End of file
                    break
                buffer.write(chunk)
    else:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDFs are accepted.")


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

# Content of ./app/routers/__init__.py:

# Content of ./app/services/auth.py:
# routers/auth.py
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from utils.config import API_KEY_NAME, PORTAL_CHAT_API_KEY

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def authenticate_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != PORTAL_CHAT_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    return api_key_header

# Content of ./app/services/openai.py:
# services/openai.py
import openai
from utils import config

openai.api_key = config.OPENAI_API_KEY
openai.organization = config.OPENAI_ORGANIZATION


def chat(chat_model: str, chat_prep: str, chat_message: str) -> str:
    # Call OpenAI API
    openai_response = openai.ChatCompletion.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": chat_prep},
            {"role": "user", "content": chat_message},
        ]
    )
    # type: ignore
    response_message = openai_response["choices"][0]["message"]["content"]
    return response_message

# Content of ./app/services/__init__.py:

# Content of ./app/utils/config.py:
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

API_KEY_NAME = "PORTAL_CHAT_API_KEY"
PORTAL_CHAT_API_KEY = get_env_variable(API_KEY_NAME)


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

# Content of ./app/utils/__init__.py:

```
