import abc
from balticlsc.balticlsc.configuration import IConfiguration


class DataHandle(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'download') and
                callable(subclass.download) and
                hasattr(subclass, 'upload') and
                callable(subclass.upload) and
                hasattr(subclass, 'check_connection') and
                callable(subclass.check_connection) or
                NotImplemented)

    @abc.abstractmethod
    def __init__(self, pin_name: str, configuration: IConfiguration):
        pass

    @abc.abstractmethod
    def download(self, handle: {}) -> str:
        pass

    @abc.abstractmethod
    def upload(self, local_path: str) -> {}:
        pass

    @abc.abstractmethod
    def check_connection(self, handle: {}):
        pass


class MongoDBHandle(DataHandle):

    def __init__(self, pin_name: str, configuration: IConfiguration):
        super().__init__(pin_name, configuration)

    def download(self, handle: {}) -> str:
        pass

    def upload(self, local_path: str) -> {}:
        pass

    def check_connection(self, handle: {}):
        pass
