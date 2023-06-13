# services/keepalive.py

import asyncio
from models.token_data import TokenData
from routers.file_man import JSONResponse
from typing import List, Optional
from services.logger import Logger

logger = Logger()


class KeepAlive:
    """
    A class used to represent the KeepAlive service

    ...

    Attributes
    ----------
    _instances : list
        a class variable to keep track of all instances of this class

    Methods
    -------
    _keepalive():
        The default implementation of the keepalive check. Can be overridden in subclasses.
    keepalive():
        Class method that calls the _keepalive method on all instances of this class.
    """

    _instances: List['KeepAlive'] = []

    def __init__(self, service_name: Optional[str]):
        self._instances.append(self)

        # add the service name to the logger
        self.service_name = service_name or __name__

    async def _keepalive(self, auth_token: Optional[TokenData]) -> JSONResponse:
        # Default implementation adds a log message with the service name
        message = f"{self.service_name} | keepalive - OK"
        logger.info(message)
        return JSONResponse(status_code=200, content={"message": message})

    @classmethod
    async def _run_keepalive(cls, instance, auth_token):
        try:
            await instance._keepalive(auth_token)
        except Exception as e:
            logger.error(f"{instance.service_name} | keepalive - ERROR: {e}")

    @classmethod
    def keepalive(cls, auth_token: Optional[TokenData]) -> JSONResponse:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            tasks = [cls._run_keepalive(instance, auth_token)
                     for instance in cls._instances]
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()
        return JSONResponse(status_code=200, content={"message": "OK"})
