# app/engine/database.py
from database_descriptor import DatabaseDescriptor


class Database:
    _instances = {}

    def __init__(self, descriptor: DatabaseDescriptor):
        self.descriptor = descriptor

    @staticmethod
    def get_instance(db_type, descriptor=None):
        if db_type not in Database._instances:
            if descriptor is None:
                raise ValueError(
                    f"No instance of {db_type} found and no descriptor provided to create one.")
            Database._instances[db_type] = db_type.create_instance(descriptor)
        return Database._instances[db_type]

    @staticmethod
    def list(db_type=None):
        if db_type is None:
            return list(Database._instances.keys())
        else:
            return [key for key in Database._instances.keys() if key == db_type]

    @classmethod
    def create_instance(cls, descriptor):
        raise NotImplementedError(
            "This method should be overridden in subclass")
