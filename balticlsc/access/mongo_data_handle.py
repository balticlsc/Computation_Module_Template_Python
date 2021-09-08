from balticlsc.scheme.configuration import IConfiguration
from balticlsc.scheme.data_handler import DataHandle


class MongoDBHandle(DataHandle):

    def __init__(self, pin_name: str, configuration: IConfiguration):
        super().__init__(pin_name, configuration)

    def download(self, handle: {}) -> str:
        pass

    def upload(self, local_path: str) -> {}:
        pass

    def check_connection(self, handle: {}):
        pass
