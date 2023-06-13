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
