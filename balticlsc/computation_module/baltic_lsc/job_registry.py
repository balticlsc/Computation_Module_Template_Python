import abc
import os
import threading
from collections import defaultdict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from balticlsc.computation_module.api_access.job_controller import JobThread

from balticlsc.computation_module.data_model.messages import Status, JobStatus, InputTokenMessage
from balticlsc.computation_module.data_model.pins_configuration import Multiplicity, PinConfiguration


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
                callable(subclass.set_variable) and
                hasattr(subclass, 'get_environment_variable') and
                callable(subclass.get_environment_variable) or
                NotImplemented)

    @abc.abstractmethod
    def get_pin_status(self, pin_name: str) -> Status:
        pass

    @abc.abstractmethod
    def get_pin_tokens(self, pin_name: str) -> []:
        pass

    @abc.abstractmethod
    def get_pin_value(self, pin_name: str) -> str or None:
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

    @abc.abstractmethod
    def get_environment_variable(self, name: str) -> str:
        pass


class JobRegistry(IJobRegistry):

    def __init__(self, pins_configuration: []):
        self.__pins = pins_configuration
        self.__tokens = defaultdict(list)
        self.__status = JobStatus(os.getenv('SYS_MODULE_INSTANCE_UID', 'module_uid'))
        self.__variables = {}
        self.__job_threads = []
        self.__semaphore = threading.Semaphore()

    def register_thread(self, thread: 'JobThread'):
        self.__semaphore.acquire()
        try:
            self.__job_threads.append(thread)
            return 0
        finally:
            self.__semaphore.release()

    def get_pin_status(self, pin_name: str) -> Status:
        self.__semaphore.acquire()
        try:
            if 0 == len(self.__tokens[pin_name]):
                return Status.IDLE
            if Multiplicity.SINGLE == self.get_pin_configuration(pin_name, False).token_multiplicity:
                return Status.COMPLETED
            final_token = next((t for t in self.__tokens[pin_name] if any(not s.is_final for s in t.token_seq_stack)),
                               None)
            if final_token is not None:
                max_count = 1
                for st in final_token.token_seq_stack:
                    max_count *= st.no + 1
                if len(self.__tokens[pin_name]) == max_count:
                    return Status.COMPLETED
            return Status.WORKING
        finally:
            self.__semaphore.release()

    def get_pin_tokens(self, pin_name: str) -> []:
        self.__semaphore.acquire()
        try:
            return self.__tokens[pin_name]
        finally:
            self.__semaphore.release()

    def get_pin_value(self, pin_name: str) -> str or None:
        (values, sizes) = self.get_pin_values_dim(pin_name)
        if values is None or 0 == len(values):
            return None
        if sizes is None and 1 == len(values):
            return values[0]
        raise Exception('Improper call - more than one token exists for the pin')

    def get_pin_values(self, pin_name: str) -> []:
        (values, sizes) = self.get_pin_values_dim(pin_name)
        if sizes is not None and 1 == len(sizes):
            return values
        raise Exception('Improper call - more than one dimension exists for the pin')

    def get_pin_values_dim(self, pin_name: str) -> ([], []):
        self.__semaphore.acquire()
        try:
            if 0 == len(self.__tokens[pin_name]):
                return None, None
            if Multiplicity.SINGLE == self.get_pin_configuration(pin_name, False).token_multiplicity:
                return [token.values for token in self.__tokens[pin_name]], None
            max_table_counts = [0] * len(next(self.__tokens[pin_name]).token_seq_stack)
            for m in self.__tokens[pin_name]:
                for i in range(len(m.token_seq_stack)):
                    if max_table_counts[i] < m.token_seq_stack[i].no:
                        max_table_counts[i] = m.token_seq_stack[i].no
            all_token_count = 1
            for i in max_table_counts:
                all_token_count *= i + 1
            result = [None] * all_token_count
            for m in self.__tokens[pin_name]:
                index = 0
                product = 1
                for i in range(len(m.token_seq_stack)):
                    index += max_table_counts[i] * product
                    product *= max_table_counts[i]
                result[index] = m.values
            return result, max_table_counts
        finally:
            self.__semaphore.release()

    def get_progress(self) -> int:
        self.__semaphore.acquire()
        try:
            return self.__status.job_progress
        finally:
            self.__semaphore.release()

    def get_job_status(self) -> JobStatus:
        self.__semaphore.acquire()
        try:
            return self.__status
        finally:
            self.__semaphore.release()

    def get_variable(self, name: str) -> object:
        self.__semaphore.acquire()
        try:
            return self.__variables[name]
        finally:
            self.__semaphore.release()

    def set_progress(self, progress: int):
        self.__semaphore.acquire()
        try:
            self.__status.job_progress = progress
        finally:
            self.__semaphore.release()

    def set_status(self, status: Status):
        self.__semaphore.acquire()
        try:
            self.__status.status = status
        finally:
            self.__semaphore.release()

    def set_variable(self, name: str, value: object):
        self.__semaphore.acquire()
        try:
            self.__variables[name] = object
        finally:
            self.__semaphore.release()

    def get_environment_variable(self, name: str) -> str:
        return os.getenv(name)

    def get_pin_configuration(self, pin_name: str, acquire: bool = True) -> PinConfiguration:
        if acquire:
            self.__semaphore.acquire()
        try:
            return next(p for p in self._JobRegistry__pins if pin_name == p.pin_name)
        finally:
            if acquire:
                self.__semaphore.release()

    def get_strong_pin_names(self) -> []:
        self.__semaphore.acquire()
        try:
            return list(p.pin_name for p in self._JobRegistry__pins if 'true' == p.is_required)
        finally:
            self.__semaphore.release()

    def get_base_msg_uid(self):
        self.__semaphore.acquire()
        try:
            return next(ltm for ltm in self._JobRegistry__tokens.values() if 0 != len(ltm))[0].msg_uid
        finally:
            self.__semaphore.release()

    def get_all_msg_uids(self):
        self.__semaphore.acquire()
        try:
            return list(it.msg_uid for pit in self._JobRegistry__tokens.values() for it in pit)
        finally:
            self.__semaphore.release()

    def clear_messages(self, msg_ids):
        for msg_id in msg_ids:
            tokens = next(ltm for ltm in self._JobRegistry__tokens.values() if any(msg_id == it.msg_uid for it in ltm))
            if tokens is not None:
                message = next(msg for msg in tokens if msg_id == msg.msg_uid)
                tokens.remove(message)

    def register_token(self, msg: InputTokenMessage):
        self.__tokens[msg.pin_name].append(msg)
