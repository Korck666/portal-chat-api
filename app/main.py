# app/main.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Import other modules after loading environment variables
from typing import List
from fastapi import FastAPI, Request, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from routers import chat, file_man, healthcheck, keepalive, ws_chat
from services.logger import Logger
from utils.cleanup import Cleanup
from utils.config import Config
from fastapi_discord import DiscordOAuthClient, RateLimited, Unauthorized, User
from fastapi_discord.exceptions import ClientSessionNotInitialized
from fastapi_discord.models import GuildPreview
from fastapi.responses import JSONResponse

logger = Logger()
config = Config()

discord = DiscordOAuthClient(
    f"{config.DISCORD_APP_ID}", 
    f"{config.DISCORD_APP_AUTH_TOKEN}", 
    "<redirect-url>", 
    ("identify", "guilds", "email")
)  # scopes



# Clean up cache
Cleanup().cleanup_cache()

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
    app.include_router(ws_chat.router)
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

    # Initialize the discord bot
@app.on_event("startup")
async def on_startup():
    try:
        logger.info("Starting discord Bot interface...")
        await discord.init()
        logger.info("Discord Bot interface started successfully. Services UP!")
    except Exception as e:
        logger.error(f"Error initializing discord chat interface: {e}")

@app.get("/login")
async def login():
    return {"url": discord.get_oauth_login_url(state="my state")}


@app.get("/callback")
async def callback(code: str, state: str):
    token, refresh_token = await discord.get_access_token(code)
    assert state == "my state"
    return {"access_token": token, "refresh_token": refresh_token}


@app.get(
    "/authenticated",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def isAuthenticated(token: str = Depends(discord.get_token)):
    try:
        auth = await discord.isAuthenticated(token)
        return auth
    except Unauthorized:
        return False


@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


@app.exception_handler(RateLimited)
async def rate_limit_error_handler(_, e: RateLimited):
    return JSONResponse(
        {"error": "RateLimited", "retry": e.retry_after, "message": e.message},
        status_code=429,
    )


@app.exception_handler(ClientSessionNotInitialized)
async def client_session_error_handler(_, e: ClientSessionNotInitialized):
    print(e)
    return JSONResponse({"error": "Internal Error"}, status_code=500)


@app.get("/user", dependencies=[Depends(discord.requires_authorization)], response_model=User)
async def get_user(user: User = Depends(discord.user)):
    return user


@app.get(
    "/guilds",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=List[GuildPreview],
)
async def get_guilds(guilds: List = Depends(discord.guilds)):
    return guilds

# shutdown on exit
@app.on_event("shutdown")
async def on_shutdown():
    try:
        logger.info("Closing discord Bot interface...")
        # await discord.init()
        logger.info("Discord Bot interface closed successfully. Services DOWN!")
    except Exception as e:
        logger.error(f"Error shutting down discord chat interface: {e}")
