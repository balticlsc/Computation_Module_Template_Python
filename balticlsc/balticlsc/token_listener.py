from os import listdir
from os.path import isfile, join
from balticlsc.balticlsc.data_handler import IDataHandler
from balticlsc.balticlsc.job_registry import IJobRegistry


class TokenListener:
    __data: IDataHandler
    __registry: IJobRegistry


class MyTokenListener(TokenListener):

    def optional_data_received(self, pin_name: str):
        # Place your code here:
        pass

    def data_received(self, pin_name: str):
        # Place your code here:
        pass

    def data_ready(self):
        # Place your code here:
        pass

    def data_complete(self):
        # Place your code here:
        folder = self.__data.obtain_data_item("Image Folder")
        files = list(f for f in listdir(folder) if isfile(join(folder, f)))
        for i in range(len(files)-1):
            self.__data.send_data_item("Images", files[i], len(files)-1 == i)
        self.__data.finish_processing()
