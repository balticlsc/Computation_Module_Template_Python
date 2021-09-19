import abc
import os
import uuid
from os import listdir
from os.path import isdir, isfile, join, basename
from shutil import rmtree
from typing import final


class DataHandle(metaclass=abc.ABCMeta):
    __baltic_data_prefix: final = 'BalticLSC-'
    __uuid_length: final = 6

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
    def __init__(self, pin_name: str, pins_configuration: []):
        self._pin_configuration = next(pc for pc in pins_configuration if pc.pin_name == pin_name)
        self._local_path = os.getenv('LOCAL_TMP_PATH', '/balticLSC_tmp')
        self._create_local()

    @abc.abstractmethod
    def download(self, handle: {}) -> str:
        pass

    @abc.abstractmethod
    def upload(self, local_path: str) -> {}:
        pass

    @abc.abstractmethod
    def check_connection(self, handle: {}):
        pass

    def _create_local(self):
        if '.' in os.path.split(self._local_path)[-1]:
            file_path = os.path.dirname(self._local_path)
        else:
            file_path = self._local_path

        if isdir(file_path):
            return

        os.mkdir(file_path)

    def _clear_local(self):
        if isdir(self._local_path):
            rmtree(self._local_path, ignore_errors=True)
        elif isfile(self._local_path):
            os.remove(self._local_path)

    def _add_guids_to_file_names(self, local_path: str):
        for f in (f for f in listdir(local_path) if isfile(join(local_path, f))):
            file_name = basename(f)
            new_file_name =\
                self.__baltic_data_prefix + str(uuid.uuid4())[:self.__uuid_length] + '-'\
                + file_name if not file_name.startswith(self.__baltic_data_prefix) else file_name[len(
                    self.__baltic_data_prefix)+self.__uuid_length:]
            os.rename(f, join(new_file_name, local_path))