from balticlsc.computation_module import init_job_controller, TokenListener
from balticlsc.computation_module.baltic_lsc.data_handler import IDataHandler
from balticlsc.computation_module import IJobRegistry


class MyTokenListener(TokenListener):

    def __init__(self, registry: IJobRegistry, data: IDataHandler):
        super().__init__(registry, data)

    def data_received(self, pin_name: str):
        # Place your code here:
        pass

    def optional_data_received(self, pin_name: str):
        # Place your code here:
        pass

    def data_ready(self):
        # Place your code here:
        pass

    def data_complete(self):
        # Place your code here:
        pass


app = init_job_controller(MyTokenListener)
