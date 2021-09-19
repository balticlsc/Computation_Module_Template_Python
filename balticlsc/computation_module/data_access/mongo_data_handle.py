import json
import os
import socket
import uuid
from os import listdir
from os.path import isdir, isfile, basename, join
from typing import Any
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError
from balticlsc.computation_module.baltic_lsc.data_handle import DataHandle
from balticlsc.computation_module.data_model.pins_configuration import Multiplicity
from balticlsc.computation_module.utils.logger import logger


def _download_single_file(document: Any, local_path: str) -> str:
    file_content = document['fileContent']
    file_path = os.path.join(local_path, document['fileName'])
    with open(file_path, mode='wb') as file:
        file.write(file_content)
    return file_path


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
        collection_name = handle['Collection']
        self.__prepare(handle['Database'], collection_name)
        local_path = ''
        match self._pin_configuration.data_multiplicity:
            case Multiplicity.SINGLE:
                if 'ObjectId' not in handle:
                    raise ValueError('Incorrect DataHandle.')
                obj_id = handle['ObjectId']
                try:
                    logger.debug('Downloading object with id: ' + obj_id)
                    document = self.__mongo_collection.find_one({'_id': ObjectId(obj_id)})
                    if document is not None:
                        local_path = _download_single_file(document, self._local_path)
                        logger.debug('Downloading object with id: ' + obj_id + ' successful.')
                    else:
                        logger.debug('Can not find object with id ' + obj_id)
                except BaseException as e:
                    logger.debug('Downloading object with id: ' + obj_id + ' failed.')
                    self._clear_local()
                    raise e
            case Multiplicity.MULTIPLE:
                try:
                    logger.debug('Downloading all files from ' + collection_name)
                    local_path = self._local_path + '/' + collection_name
                    os.mkdir(local_path)
                    documents = self.__mongo_collection.find()
                    for doc in documents:
                        _download_single_file(doc, local_path)
                    self._add_guids_to_file_names(local_path)
                    logger.debug('Downloading all files from ' + collection_name + ' successful.')
                except BaseException as e:
                    logger.debug('Downloading all files from ' + collection_name + ' failed.')
                    self._clear_local()
                    raise e
        return local_path

    def upload(self, local_path: str) -> {}:
        if "output" != self._pin_configuration.pin_type:
            raise Exception('Upload cannot be called for input pins')
        if not isfile(local_path) and not isdir(local_path):
            raise ValueError('Invalid path (' + local_path + ')')
        is_directory = isdir(local_path)
        if Multiplicity.MULTIPLE == self._pin_configuration.data_multiplicity and not is_directory:
            raise ValueError('Multiple data pin requires path pointing to a directory, not a file')
        if Multiplicity.SINGLE == self._pin_configuration.data_multiplicity and is_directory:
            raise ValueError('Single data pin requires path pointing to a file, not a directory')
        handle = {}
        try:
            database_name, collection_name = self.__prepare()
            match self._pin_configuration.data_multiplicity:
                case Multiplicity.SINGLE:
                    logger.debug('Uploading file from ' + local_path + 'to collection ' + collection_name)
                    file_name = basename(local_path)
                    with open(local_path, mode='rb') as file:
                        file_content = file.read()
                    result = self.__mongo_collection.insert_one({'fileName': file_name,
                                                                 'fileContent': file_content})
                    handle = {'FileName': file_name, 'ObjectId': str(result.inserted_id), 'Database': database_name,
                              'Collection': collection_name}
                    logger.debug('Uploading file from ' + local_path + ' to collection ' + collection_name +
                                 ' successful.')
                case Multiplicity.MULTIPLE:
                    logger.debug('Uploading directory from ' + local_path + ' to collection ' + collection_name)
                    handle_list = []
                    for f in (f for f in listdir(local_path) if isfile(join(local_path, f))):
                        file_name = basename(f)
                        with open(f, mode='rb') as file:
                            file_content = file.read()
                        result = self.__mongo_collection.insert_one({'fileName': file_name,
                                                                     'fileContent': file_content})
                        handle_list.append({'FileName': file_name, 'ObjectId': str(result.inserted_id)})
                    handle = {'Files': json.dumps(handle_list), 'Database': database_name,
                              'Collection': collection_name}
                    logger.Debug('Uploading directory from ' + local_path + 'to collection ' + collection_name +
                                 ' successful.')
            return handle
        except BaseException as e:
            logger.Debug('Error: ' + str(e) + ' \n Uploading from ' + local_path + ' failed.')
            raise e
        finally:
            self._clear_local()

    def check_connection(self, handle: {}):
        '''
        host = self._pin_configuration.access_credential["Host"]
        port = int(self._pin_configuration.access_credential["Port"])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            if not sock.connect_ex((host, port)):
                logger.debug(f'Unable to reach {host}:{port}')
                return -1
        finally:
            sock.close()
        '''
        logger.debug(f'MongoDB connection string: {self.__connection_string}')

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
