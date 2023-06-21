import asyncio
from typing import Callable, Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jwt import PyJWTError
from models.token_data import TokenData
from services.logger import Logger
from services.mongodb import MongoDB
from utils.config import Config


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


# import requests
# from app.config import Config
# import discord


# class Authenticator:
#     def __init__(self, client_id, client_secret, redirect_uri, scope):
#         self.config = Config()
#         self.client_id = client_id
#         self.client_secret = client_secret
#         self.redirect_uri = redirect_uri
#         self.scope = scope

#     def generate_discord_oauth_url(self):
#         """
#         Generates the Discord OAuth URL.

#         :return: The Discord OAuth URL.
#         """
#         return f'https://discord.com/api/oauth2/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}'

#     def exchange_authorization_code_for_access_token(self, code):
#         """
#         Exchanges the authorization code for an access token.

#         :param code: The authorization code.
#         :return: The access token.
#         """
#         data = {
#             'client_id': self.client_id,
#             'client_secret': self.client_secret,
#             'grant_type': 'authorization_code',
#             'code': code,
#             'redirect_uri': self.redirect_uri,
#             'scope': self.scope
#         }

#         headers = {
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }

#         response = requests.post(
#             'https://discord.com/api/oauth2/token', data=data, headers=headers)

#         if response.status_code == 200:
#             return response.json()['access_token']
#         else:
#             raise Exception(
#                 'Failed to exchange authorization code for access token')

#     def get_discord_profile_info(self, access_token):
#         """
#         Retrieves the user's Discord profile information.

#         :param access_token: The access token.
#         :return: The user's Discord profile information.
#         """
#         headers = {
#             'Authorization': f'Bearer {access_token}'
#         }

#         response = requests.get(
#             'https://discord.com/api/users/@me', headers=headers)

#         if response.status_code == 200:
#             return response.json()
#         else:
#             raise Exception('Failed to retrieve Discord profile information')
