from pydantic import BaseModel
import os
import openai
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


def get_env_variable(variable_name: str) -> str:
    """
    Returns the value of the given environment variable or an empty string if it is not set.
    """
    value = os.getenv(variable_name)
    return value if value is not None else ""


workdir = get_env_variable("PWD")
app = FastAPI(docs_url=None, redoc_url=None,
              title="AI backend engine API",
              version="0.1.0",
              description="Portal Chat API - internal service",
              )

app.mount(f"{workdir}/static", StaticFiles(directory="static"), name="static")


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


openai.api_key = get_env_variable("OPENAI_API_KEY")


# your app code here...


class ChatInput(BaseModel):
    message: str


class ChatOutput(BaseModel):
    response: str


@app.post("/chat", response_model=ChatOutput)
def chat_endpoint(chat_input: ChatInput):
    # Call OpenAI API
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": chat_input.message},
        ]
    )
    # type: ignore
    response_message = openai_response["choices"][0]["message"]["content"] # type: ignore
    # Return the response
    return ChatOutput(response=response_message)
