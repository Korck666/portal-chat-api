# services/keepalive.py

import asyncio
import time
from models.token_data import TokenData
from routers.file_man import JSONResponse
from services.logger import logger
from typing import List, Optional


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

    def __init__(self, service_name: Optional[str]):
        self._instances.append(self)
        # add the service name to the logger
        self.service_name = service_name or __name__

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
            response = await task
            end_time = time.time()
            response_time = end_time - start_time
            responses.append(JSONResponse(status_code=200, content={
                             "message": response.json().get("message"), "response_time": response_time}))
        return responses
