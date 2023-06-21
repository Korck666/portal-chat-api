# app/services/ngrok.py
import logging
from fastapi import FastAPI
from utils.config import Config
from services.logger import Logger
import ngrok


class NgrokService():
    _intance: 'NgrokService'
    _app: FastAPI

    @classmethod
    def __new__(cls, app: FastAPI) -> "NgrokService":
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._app = app
            cls.config = Config()
            cls.logger = Logger()
            cls.ngrok = ngrok.Client(cls.config.NGROK_AUTH_TOKEN)
            cls.client = cls.ngrok.ip_policies.create()
            cls.logger.info("NgrokService initialized.")

        return cls._instance
