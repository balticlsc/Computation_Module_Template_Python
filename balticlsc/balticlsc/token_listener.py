import abc
from balticlsc.balticlsc.data_handler import IDataHandler
from balticlsc.balticlsc.job_registry import IJobRegistry


class TokenListener:

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'data_received') and
                callable(subclass.data_received) and
                hasattr(subclass, 'optional_data_received') and
                callable(subclass.optional_data_received) and
                hasattr(subclass, 'data_ready') and
                callable(subclass.data_ready) and
                hasattr(subclass, 'data_complete') and
                callable(subclass.data_complete) or
                NotImplemented)

    @abc.abstractmethod
    def __init__(self, registry: IJobRegistry, data: IDataHandler):
        _data = data
        _registry = registry

    @abc.abstractmethod
    def data_received(self, pin_name: str):
        pass

    @abc.abstractmethod
    def optional_data_received(self, pin_name: str):
        pass

    @abc.abstractmethod
    def data_ready(self):
        pass

    @abc.abstractmethod
    def data_complete(self):
        pass


class MyTokenListener(TokenListener):

    def __init__(self, registry: IJobRegistry, data: IDataHandler):
        super().__init__(registry, data)

    def data_received(self, pin_name: str):
        # Place your code here:
        pass

    def optional_data_received(self, pin_name: str):
        # Place your code here:
        pass

    def data_ready(self):
        # Place your code here:
        pass

    def data_complete(self):
        # Place your code here:
        pass
