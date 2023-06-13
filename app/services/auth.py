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
