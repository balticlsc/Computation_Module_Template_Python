from balticlsc.balticlsc.data_handler import DataHandler
from balticlsc.balticlsc.job_registry import JobRegistry
from balticlsc.balticlsc.messages import Status
from balticlsc.balticlsc.token_listener import TokenListener


class JobThread:

    def __init__(self, pin_name: str, listener: TokenListener, registry: JobRegistry, handler: DataHandler):
        self.__pin_name = pin_name
        self.__listener = listener
        self.__registry = registry
        self.__handler = handler

    def run(self):
        try:
            self.__listener.data_received(self.__pin_name)
            if "true" == self.__registry.get_pin_configuration(self.__pin_name).is_required:
                self.__listener.optional_data_received(self.__pin_name)
            pin_aggregated_status = Status.COMPLETED
            for pin_name in self.__registry.get_strong_pin_names():
                pin_status = self.__registry.get_pin_status(pin_name)
                if Status.WORKING == pin_status:
                    pin_aggregated_status = Status.WORKING
                elif Status.IDLE == pin_status:
                    pin_aggregated_status = Status.IDLE
                    break
            if Status.IDLE != pin_aggregated_status:
                self.__listener.data_ready()
            if Status.COMPLETED == pin_aggregated_status:
                self.__listener.data_complete()
        except Exception as e:
            self.__handler.fail_processing(str(e))
