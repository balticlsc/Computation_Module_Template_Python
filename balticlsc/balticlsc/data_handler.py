import abc
import json
from typing import Dict
from balticlsc.balticlsc.data_handle import DataHandle
from balticlsc.balticlsc.job_registry import JobRegistry


class IDataHandler(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'obtain_data_item') and
                callable(subclass.obtain_data_item) and
                hasattr(subclass, 'obtain_data_items') and
                callable(subclass.obtain_data_items) and
                hasattr(subclass, 'obtain_data_items_dim') and
                callable(subclass.obtain_data_items_dim) and
                hasattr(subclass, 'send_data_item') and
                callable(subclass.send_data_item) and
                hasattr(subclass, 'send_token') and
                callable(subclass.send_token) and
                hasattr(subclass, 'finish_processing') and
                callable(subclass.finish_processing) and
                hasattr(subclass, 'send_ack_token') and
                callable(subclass.send_ack_token) or
                NotImplemented)

    @abc.abstractmethod
    def obtain_data_item(self, pin_name: str) -> str or None:
        pass

    @abc.abstractmethod
    def obtain_data_items(self, pin_name: str) -> []:
        pass

    @abc.abstractmethod
    def obtain_data_items_dim(self, pin_name: str) -> ([], []):
        pass

    @abc.abstractmethod
    def send_data_item(self, pin_name: str, data: str, is_final: bool, msg_uid: str = None) -> int:
        pass

    @abc.abstractmethod
    def send_token(self, pin_name: str, values: str, is_final: bool, msg_uid: str = None) -> int:
        pass

    @abc.abstractmethod
    def finish_processing(self) -> int:
        pass

    @abc.abstractmethod
    def send_ack_token(self, msg_ids: [], is_final: bool) -> int:
        pass


class DataHandler(IDataHandler):

    def __init__(self, registry: JobRegistry):
        self.__registry = registry

    def obtain_data_item(self, pin_name: str) -> str or None:
        (values, sizes) = self.obtain_data_items_dim(pin_name);
        if values is None or 0 == values.count():
            return None
        if sizes is None and 1 == values.count():
            return values[0]
        raise Exception("Improper call - more than one data item exists for the pin")

    def obtain_data_items(self, pin_name: str) -> []:
        (values, sizes) = self.obtain_data_items_dim(pin_name);
        if sizes is not None and 1 == sizes.count():
            return values
        raise Exception("Improper call - more than one dimension exists for the pin")

    def obtain_data_items_dim(self, pin_name: str) -> ([], []):
        (values, sizes) = self.__registry.get_pin_values_dim(pin_name)
        values_object = list(map(lambda v: None if v is None or not v else json.load(v), values))
        handle = self.get_data_handle(pin_name)
        data_items = list(map(lambda vo: None if vo is None else handle.download(vo), values_object))
        return data_items, sizes

    def send_data_item(self, pin_name: str, data: str, is_final: bool, msg_uid: str = None) -> int:
        pass

    def send_token(self, pin_name: str, values: str, is_final: bool, msg_uid: str = None) -> int:
        pass

    def finish_processing(self) -> int:
        pass

    def send_ack_token(self, msg_ids: [], is_final: bool) -> int:
        pass

    def fail_processing(self, note: str):
        pass

    def check_connection(self, pin_name: str, handle: Dict[str, str] = None) -> int:
        pass

    def get_data_handle(self, pin_name:str) -> DataHandle:
        pass
