import socket
import uuid
from os.path import isdir, isfile
from typing import Any
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError
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
        self.__mongo_client = None
        self.__mongo_database = None
        self.__mongo_collection = None

    def download(self, handle: {}) -> str:
        if "input" != self._pin_configuration.pin_type:
            raise Exception('Download cannot be called for output pins')
        if 'Database' not in handle:
            raise ValueError('Incorrect DataHandle.')
        if 'Collection' not in handle:
            raise ValueError('Incorrect DataHandle.')
        self.__prepare(handle['Database'], handle['Collection'])
        local_path = ''
        match self._pin_configuration.data_multiplicity:
            case Multiplicity.SINGLE:
                if 'ObjectId' not in handle:
                    raise ValueError('Incorrect DataHandle.')
                obj_id = handle['ObjectId']
                try:
                    document = self.__mongo_collection.find_one({'_id': ObjectId(obj_id)})
                    if document is not None:
                        local_path = self.__download_single_file(document, self._local_path)
                        logger.debug('Downloading object with id: ' + obj_id + ' successful.')
                    else:
                        logger.debug('Can not find object with id ' + obj_id)
                except PyMongoError as e:
                    logger.debug('Downloading object with id: ' + obj_id + ' failed.')
                    self._clear_local()
                    raise e
            case Multiplicity.MULTIPLE:
                pass
        return local_path

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
                    logger.debug('Uploading file from ' + self._local_path + 'to collection ' + collection_name)
                    pass
                case Multiplicity.MULTIPLE:
                    logger.debug('Uploading directory from ' + self._local_path + 'to collection ' + collection_name)
                    pass
            return handle
        except BaseException as e:
            logger.Debug('Error: ' + str(e) + ' \n Uploading from ' + self._local_path + ' failed.')
            raise e
        finally:
            self._clear_local()

    def check_connection(self, handle: {}):
        host = self._pin_configuration.access_credential["Host"]
        port = self._pin_configuration.access_credential["Port"]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if not sock.connect_ex((host, port)):
                logger.debug('Unable to reach ' + host + ':' + port)
                return -1
        finally:
            sock.close()
        try:
            self.__mongo_client = MongoClient(self.__connection_string)
            self.__mongo_client.list_databases()
        except OperationFailure:  # TODO check if authorization error (if needed)
            logger.debug('Unable to authenticate to MongoDB')
            return -2
        except PyMongoError as e:
            logger.debug('Error ' + str(e) + ' while trying to connect to MongoDB')
            return -1
        if 'input' == self._pin_configuration.pin_type and handle is not None:
            if 'Database' not in handle:
                raise ValueError('Incorrect DataHandle.')
            if 'Collection' not in handle:
                raise ValueError('Incorrect DataHandle.')
            database_name = handle['Database']
            collection_name = handle['Collection']
            if Multiplicity.SINGLE == self._pin_configuration.data_multiplicity and 'ObjectId' not in handle:
                raise ValueError('Incorrect DataHandle.')
            obj_id = handle['ObjectId']
            try:
                self.__mongo_database = self.__mongo_client[database_name]
                if self.__mongo_database is None:
                    logger.debug('No database ' + database_name)
                    return -3
                self.__mongo_collection = self.__mongo_database[collection_name]
                if self.__mongo_collection is None:
                    logger.debug('No collection ' + database_name)
                    return -3
                if Multiplicity.SINGLE == self._pin_configuration.data_multiplicity:
                    document = self.__mongo_collection.find_one({'_id': ObjectId(obj_id)})
                    if document is None:
                        logger.debug('No document with id ' + obj_id)
                        return -3
            except PyMongoError:
                logger.debug('Error while trying to ' +
                             ('access collection ' + collection_name if obj_id is None else 'get object ' + obj_id)
                             + ' from database ' + database_name +
                             ('' if obj_id is None else ' from collection ' + collection_name))
                return -3
        return 0

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

    def __download_single_file(self, document: Any, _local_path: str) -> str:
        pass
