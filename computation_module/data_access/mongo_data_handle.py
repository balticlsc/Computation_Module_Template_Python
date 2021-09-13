from computation_module.baltic_lsc.data_handler import DataHandle


class MongoDBHandle(DataHandle):

    def __init__(self, pin_name: str, pins_configuration: []):
        super().__init__(pin_name, pins_configuration)

    def download(self, handle: {}) -> str:
        if "input" != self._pin_configuration.pin_type:
            raise Exception('Download cannot be called for output pins')
        if 'Database' not in handle:
            raise ValueError('Incorrect DataHandle.')
        if 'Collection' not in handle:
            raise ValueError('Incorrect DataHandle.')
        pass

    def upload(self, local_path: str) -> {}:
        if "output" != self._pin_configuration.pin_type:
            raise Exception('Upload cannot be called for input pins')
        pass

    def check_connection(self, handle: {}):
        pass
