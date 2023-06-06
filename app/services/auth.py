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
