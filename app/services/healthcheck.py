import asyncio
import time

from typing import List, Optional
from routers.file_man import JSONResponse
from models.token_data import TokenData
from services.logger import Logger

logger = Logger()


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

    def __init__(self, service_name: Optional[str] = None):
        self.service_name = service_name or __name__
        self._instances.append(self)

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
            response: Optional[JSONResponse] = await task
            end_time = time.time()
            response_time = end_time - start_time
            if response is not None:
                responses.append(JSONResponse(status_code=200, content={
                    "message": response.body[slice("message", "message" + "\0")], "response_time": response_time}))
        return responses
