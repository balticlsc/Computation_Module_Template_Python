import uuid
from os.path import isdir, isfile
from pymongo import MongoClient
from computation_module.baltic_lsc.data_handler import DataHandle
from computation_module.data_model.pins_configuration import Multiplicity
from computation_module.utils.logger import logger


class MongoDBHandle(DataHandle):

    def __init__(self, pin_name: str, pins_configuration: []):
        super().__init__(pin_name, pins_configuration)
        self.__connection_string = 'mongodb://' + self._pin_configuration.access_credential['User'] + ':' \
                                   + self._pin_configuration.access_credential['Password'] + '@' \
                                   + self._pin_configuration.access_credential['Host'] + ':' \
                                   + self._pin_configuration.access_credential['Port']

    def download(self, handle: {}) -> str:
        if "input" != self._pin_configuration.pin_type:
            raise Exception('Download cannot be called for output pins')
        if 'Database' not in handle:
            raise ValueError('Incorrect DataHandle.')
        if 'Collection' not in handle:
            raise ValueError('Incorrect DataHandle.')
        self.__prepare(handle['Database'], handle['Collection'])
        pass

    def upload(self, local_path: str) -> {}:
        if "output" != self._pin_configuration.pin_type:
            raise Exception('Upload cannot be called for input pins')
        if not isfile(self._local_path) and not isdir(self._local_path):
            raise ValueError('Invalid path (' + self._local_path + ')')
        is_directory = isdir(self._local_path)
        if Multiplicity.MULTIPLE == self._pin_configuration.data_multiplicity and not is_directory:
            raise ValueError('Multiple data pin requires path pointing to a directory, not a file')
        if Multiplicity.SINGLE == self._pin_configuration.data_multiplicity and is_directory:
            raise ValueError('Single data pin requires path pointing to a file, not a directory')
        handle = {}
        try:
            database_name, collection_name = self.__prepare()
            match self._pin_configuration.data_multiplicity:
                case Multiplicity.SINGLE:
                    pass
                case Multiplicity.MULTIPLE:
                    pass
            pass
        except BaseException as e:
            logger.Debug('Error: ' + str(e) + ' \n Uploading from ' + self._local_path + ' failed.')
            raise e
        finally:
            self._clear_local()

    def check_connection(self, handle: {}):
        host = self._pin_configuration.access_credential["Host"]
        port = self._pin_configuration.access_credential["Port"]
        pass

    def __prepare(self, database_name: str = None, collection_name: str = None) -> (str, str):
        if database_name is None:
            database_name = 'baltic_database_' + str(uuid.uuid4())[:8]
        if collection_name is None:
            collection_name = 'baltic_collection_' + str(uuid.uuid4())[:8]
        # TODO to reset or not to reset
        self.__mongo_client = MongoClient(self.__connection_string)
        self.__mongo_database = self.__mongo_client[database_name]
        self.__mongo_collection = self.__mongo_database[collection_name]
        return database_name, collection_name
