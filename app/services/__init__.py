class services:
    """
    A module used to represent the services package

    ...

    Attributes
    ----------
    __all__ : list
        a list of all modules in the package

    Methods
    -------
    """
    __all__: list[str] = ['auth', 'healthcheck',
                          'keepalive', 'mongodb',
                          'openai', 'logger']

    @classmethod
    def services(cls) -> list[str]:
        return cls.__all__
