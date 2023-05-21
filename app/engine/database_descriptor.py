# database_descriptor.py
from app.engine.database_type import DatabaseType


class DatabaseDescriptor:
    def __init__(self, db_type: DatabaseType, host: str, port: int, user: str, environment: str,
                 db_name: str, password: str, api_key: str, namespace: str = 'default', log_level: str = 'INFO',
                 config: str = '', openapi_config: str = '', *args, **kwargs):

        self.db_type = db_type
        self.host = host
        self.port = port
        self.user = user
        self.environment = environment
        self.password = password
        self.db_name = db_name
        self.api_key = api_key
        self.namespace = namespace
        self.log_level = log_level
        self.config = config
        self.openapi_config = openapi_config
        self.args = args
        self.kwargs = kwargs

        # we use hash to make sure that the descriptor is unique
        # and can be used as a key in a dictionary
        # this is important for the database factory
        # which uses a dictionary to store the database instances
        # and retrieve them by descriptor
        # it is also a quick way to invalidate the cache
        # if the descriptor changes
        self.hash = hash((self.db_type, self.host, self.port,
                          self.user, self.password, self.api_key,
                          self.namespace, self.log_level, self.config,
                          self.openapi_config, self.args, self.kwargs))
