import abc
import enum
from balticlsc.balticlsc.messages import Status


class IJobRegistry(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_pin_status') and
                callable(subclass.get_pin_status) and
                hasattr(subclass, 'get_pin_tokens') and
                callable(subclass.get_pin_tokens) and
                hasattr(subclass, 'get_pin_value') and
                callable(subclass.get_pin_value) and
                hasattr(subclass, 'get_pin_values') and
                callable(subclass.get_pin_values) and
                hasattr(subclass, 'get_pin_values_dim') and
                callable(subclass.get_pin_values_dim) and
                hasattr(subclass, 'get_progress') and
                callable(subclass.get_progress) and
                hasattr(subclass, 'get_variable') and
                callable(subclass.get_variable) and
                hasattr(subclass, 'set_progress') and
                callable(subclass.set_progress) and
                hasattr(subclass, 'set_status') and
                callable(subclass.set_status) and
                hasattr(subclass, 'set_variable') and
                callable(subclass.set_variable) or
                NotImplemented)

    @abc.abstractmethod
    def get_pin_status(self, pin_name: str) -> Status:
        pass

    @abc.abstractmethod
    def get_pin_tokens(self, pin_name: str) -> []:
        pass

    @abc.abstractmethod
    def get_pin_value(self, pin_name: str) -> str:
        pass

    @abc.abstractmethod
    def get_pin_values(self, pin_name: str) -> []:
        pass

    @abc.abstractmethod
    def get_pin_values_dim(self, pin_name: str) -> ([], []):
        pass

    @abc.abstractmethod
    def get_progress(self) -> int:
        pass

    @abc.abstractmethod
    def get_variable(self, name: str) -> object:
        pass

    @abc.abstractmethod
    def set_progress(self, progress: int):
        pass

    @abc.abstractmethod
    def set_status(self, status: Status):
        pass

    @abc.abstractmethod
    def set_variable(self, name: str, value: object):
        pass


class Multiplicity(enum.Enum):
    SINGLE = 0
    MULTIPLE = 1


class PinConfiguration:
    pin_name: str
    pin_type: str
    is_required: str
    token_multiplicity: Multiplicity
    data_multiplicity: Multiplicity
    access_type: str
    access_credential: str


class JobRegistry(IJobRegistry):

    def get_pin_status(self, pin_name: str) -> Status:
        pass

    def get_pin_tokens(self, pin_name: str) -> []:
        pass

    def get_pin_value(self, pin_name: str) -> str:
        pass

    def get_pin_values(self, pin_name: str) -> []:
        pass

    def get_pin_values_dim(self, pin_name: str) -> ([], []):
        pass

    def get_progress(self) -> int:
        pass

    def get_variable(self, name: str) -> object:
        pass

    def set_progress(self, progress: int):
        pass

    def set_status(self, status: Status):
        pass

    def set_variable(self, name: str, value: object):
        pass

    def get_pin_configuration(self, pin_name: str) -> PinConfiguration:
        pass

    def get_strong_pin_names(self) -> []:
        pass
