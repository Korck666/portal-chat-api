# game_system.py
from abc import abstractmethod


class GameSystem:
    _context = {}

    @staticmethod
    def get_context(descriptor=None):
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
    def __init__(self, game_state):
        self.game_state = game_state

    @abstractmethod
    def apply(self, game_state):
        raise NotImplementedError
