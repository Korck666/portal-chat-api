# app/engine/database_descriptor.py
from app.engine.database_type import DatabaseType
from app.engine.descriptor import Descriptor
from app.engine.log_level import LogLevel

# this class should contain all the information needed to create a database instance


class DatabaseDescriptor(Descriptor):

    def __init__(self, db_type: DatabaseType, host: str, port: int, user: str,
                 environment: str, db_name: str, password: str, api_key: str,
                 namespace: str = 'default', config: str = '', openapi_config: dict = {},
                 log_level: LogLevel = LogLevel.INFO, args: tuple = (), kwargs: dict = {}) -> None:
        super().__init__(log_level=log_level)
        self.db_type = db_type
        self.host = host
        self.port = port
        self.user = user
        self.environment = environment
        self.db_name = db_name
        self.password = password
        self.api_key = api_key
        self.namespace = namespace
        self.config = config
        self.openapi_config = openapi_config
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def from_dict(db_dict: dict):
        return DatabaseDescriptor(
            db_type=db_dict['db_type': DatabaseType],
            host=db_dict['host': str],
            port=db_dict['port': int],
            user=db_dict['user': str],
            environment=db_dict['environment': str],
            db_name=db_dict['db_name': str],
            password=db_dict['password': str],
            api_key=db_dict['api_key': str],
            namespace=db_dict['namespace': str] | 'default',
            log_level=db_dict['log_level': str] | 'INFO',
            config=db_dict['config': str] | '',
            openapi_config=db_dict['openapi_config': dict] | {},
            args=db_dict['args': tuple] | (),
            kwargs=db_dict['kwargs': dict] | {})
