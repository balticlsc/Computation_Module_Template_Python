import json
import numpy
from numpy import ndarray, asarray
from pyswarms import backend
from pyswarms.backend.topology import Star
from computation_module.api_access.job_controller import init_job_controller, TokenListener
from computation_module.baltic_lsc.data_handler import IDataHandler
from computation_module.baltic_lsc.job_registry import IJobRegistry
from computation_module.data_model.messages import Status


def from_numpy_dict(source: {}) -> {}:
    return {key: asarray(value) if isinstance(value, type([])) else value for key, value in source.items()}


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
        self._registry.set_status(Status.WORKING)
        swarm_file_path = self._data.obtain_data_item('current swarm')
        with open(swarm_file_path) as swarm_file:
            swarm = backend.Swarm(**{key: value.tolist() if isinstance(value, ndarray) else value for key, value
                                     in json.load(swarm_file)})
        swarm.current_cost = asarray(list(json.loads(c)['value'] for c
                                          in self._registry.get_pin_values('Population Fitness')))
        swarm.pbest_pos, swarm.pbest_cost = backend.compute_pbest(swarm)
        topology = Star()
        if numpy.min(swarm.pbest_cost) < swarm.best_cost:
            swarm.best_pos, swarm.best_cost = topology.compute_gbest(swarm)
        swarm.velocity = topology.compute_velocity(swarm)
        swarm.position = topology.compute_position(swarm)
        data_set_handle = self._registry.get_pin_value('current data set')
        for i in range(len(swarm.position)):
            self._data.send_data_item('population', json.dumps(swarm.position[i].tolist()),
                                      len(swarm.position) == len(swarm.position) - 1)
            self._data.send_data_item('data sets', data_set_handle,
                                      len(swarm.position) == len(swarm.position) - 1)
        self._data.send_data_item('next data set', data_set_handle, True)
        with open('swarm.json', 'w') as f:
            json.dump({key: asarray(value) if isinstance(value, type([])) else value for key, value
                       in swarm.__dict__.items()}, f)
        self._data.send_token('next swarm', 'swarm.json', True)
        self._data.finish_processing()


app = init_job_controller(MyTokenListener)
