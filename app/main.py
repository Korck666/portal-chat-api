from logging import log
from services.logger import logger
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from fastapi import FastAPI
from utils import config
from routers import file_man, chat

logger.info("Starting app...")
logger.info(f"WORKDIR: {config.WORKDIR}")
logger.info(f"CHAT_MODEL: {config.CHAT_MODEL}")
logger.info(
    f"read|write f block: {config.FILE_CHUNCK[config.DEFAULT_FILE_CHUNCK_INDEX]} bytes")
logger.info(f"{config.API_TITLE} v{config.API_VERSION}")
logger.info(f"{config.API_DESCRIPTION}")


app = FastAPI(docs_url=None, redoc_url=None,
              title=config.API_TITLE,
              version=config.API_VERSION,
              description=config.API_DESCRIPTION,
              )

logger.info("Adding static files...")

app.mount(f"{config.WORKDIR}/static",
          StaticFiles(directory="static"), name="static")


logger.info("Adding routers...")
# swagger


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
logger.info("Adding routers...")


@app.get("/")
def home():
    return RedirectResponse("/docs")


# add routers
app.include_router(file_man.router)
app.include_router(chat.router)
