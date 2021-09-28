import abc
import json
from http import HTTPStatus
from typing import Dict

from balticlsc.computation_module.baltic_lsc.data_handle import DataHandle
from balticlsc.computation_module.data_access.mongo_data_handle import MongoDBHandle
from balticlsc.computation_module.baltic_lsc.job_registry import JobRegistry
from balticlsc.computation_module.data_model.messages import Status
from balticlsc.computation_module.api_access.tokens_proxy import TokensProxy


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

    def __init__(self, registry: JobRegistry, pins_configuration: []):
        self.__registry = registry
        self.__pins_configuration = pins_configuration
        self.__tokens_proxy = TokensProxy()
        self.__data_handles = {}

    def obtain_data_item(self, pin_name: str) -> str or None:
        (values, sizes) = self.obtain_data_items_dim(pin_name)
        if values is None or 0 == len(values):
            return None
        if sizes is None and 1 == len(values):
            return values[0]
        raise Exception('Improper call - more than one data item exists for the pin')

    def obtain_data_items(self, pin_name: str) -> []:
        (values, sizes) = self.obtain_data_items_dim(pin_name)
        if sizes is not None and 1 == len(sizes):
            return values
        raise Exception('Improper call - more than one dimension exists for the pin')

    def obtain_data_items_dim(self, pin_name: str) -> ([], []):
        (values, sizes) = self.__registry.get_pin_values_dim(pin_name)
        values_object = list(map(lambda v: None if v is None or not v else json.loads(v), values))
        d_handle = self.get_data_handle(pin_name)
        data_items = list(map(lambda vo: None if vo is None else d_handle.download(vo), values_object))
        return data_items, sizes

    def send_data_item(self, pin_name: str, data: str, is_final: bool, msg_uid: str = None) -> int:
        d_handle = self.get_data_handle(pin_name)
        new_handle = d_handle.upload(data)
        return self.send_token(pin_name, json.dumps(new_handle), is_final, msg_uid)

    def send_token(self, pin_name: str, values: str, is_final: bool, msg_uid: str = None) -> int:
        if msg_uid is None:
            msg_uid = self.__registry.get_base_msg_uid()

        return 0 if HTTPStatus.OK == self._DataHandler__tokens_proxy.send_output_token(pin_name, values, msg_uid, is_final) else -1

    def finish_processing(self) -> int:
        msg_ids = self.__registry.get_all_msg_uids()
        self.__registry.set_status(Status.COMPLETED)
        return self.send_ack_token(msg_ids, True)

    def fail_processing(self, note: str):
        msg_ids = self.__registry.get_all_msg_uids()
        self.__registry.set_status(Status.FAILED)
        if HTTPStatus.OK == self._DataHandler__tokens_proxy.send_ack_token(msg_ids, True, True, note):
            self.__registry.clear_messages(msg_ids)
            return 0
        return -1

    def send_ack_token(self, msg_ids: [], is_final: bool) -> int:
        if HTTPStatus.OK == self._DataHandler__tokens_proxy.send_ack_token(msg_ids, is_final):
            self.__registry.clear_messages(msg_ids)
            return 0

        return -1

    def check_connection(self, pin_name: str, handle: Dict[str, str] = None) -> int:
        try:
            d_handle = self.get_data_handle(pin_name)
            return d_handle.check_connection(handle)
        except ValueError:
            raise ValueError('Cannot check connection for a pin of type \"Direct\"')

    def get_data_handle(self, pin_name: str) -> DataHandle:
        if pin_name in self.__data_handles:
            return self.__data_handles[pin_name]
        access_type = self.__registry.get_pin_configuration(pin_name).access_type
        match access_type:
            case 'Direct':
                raise ValueError('Cannot create a data handle for a pin of type \"Direct\"')
            case '':
                handle = MongoDBHandle(pin_name, self.__pins_configuration)
            case _:
                raise NotImplementedError('AccessType (' + access_type + ') not supported by the DataHandler, has to '
                                                                         'be handled manually')
        self.__data_handles[pin_name] = handle
        return handle
