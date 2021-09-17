from computation_module.api_access.job_controller import init_job_controller, TokenListener
from computation_module.baltic_lsc.data_handler import IDataHandler
from computation_module.baltic_lsc.job_registry import IJobRegistry

# Import modules
import numpy as np

# Import sphere function as objective function
from pyswarms.utils.functions.single_obj import sphere as f

# Import backend modules
import pyswarms.backend as P
from pyswarms.backend.topology import Star


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
