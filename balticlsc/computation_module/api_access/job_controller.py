import json
import os
import threading
import traceback
from typing import Type, Optional
from flask import Flask, request, Response
from balticlsc.computation_module.baltic_lsc.data_handler import DataHandler
from balticlsc.computation_module.baltic_lsc.job_registry import JobRegistry
from balticlsc.computation_module.baltic_lsc.job_engine import TokenListener, JobThread
from balticlsc.computation_module.utils.logger import logger
from balticlsc.computation_module.data_model.messages import InputTokenMessage, SeqToken
from balticlsc.computation_module.data_model.pins_configuration import get_pins_configuration
from balticlsc.computation_module.utils.utils import camel_dict_to_snake_dict, snake_dict_to_camel_dict

__registry: Optional[JobRegistry] = None
__handler: Optional[DataHandler] = None
__listener_type: Optional[Type[TokenListener]] = None


def init_job_controller(listener_type: Type[TokenListener]) -> Flask:
    global __listener_type, __registry, __handler
    __listener_type = listener_type
    pins_configuration = get_pins_configuration()
    __registry = JobRegistry(pins_configuration)
    __handler = DataHandler(__registry, pins_configuration)
    app = Flask(os.getenv('SYS_MODULE_NAME', 'BalticLSC module'))

    @app.route('/token', methods=['POST'])
    def process_token():
        try:
            logger.debug('Token message received: ' + str(request.json))
            input_token = InputTokenMessage(
                **{key: value if 'token_seq_stack' != key else list(
                    SeqToken(**in_value) for in_value in json.loads(value))
                   for key, value in camel_dict_to_snake_dict(request.json).items() if key in
                   InputTokenMessage.__dict__['__annotations__']})
            __registry.register_token(input_token)
            try:
                result = __handler.check_connection(input_token.pin_name, json.loads(input_token.values))
                match result:
                    case 0:
                        logger.debug(f'Running job for pin "{input_token.pin_name}"')
                        job_thread = JobThread(input_token.pin_name, __listener_type(__registry, __handler),
                                               __registry, __handler)
                        __registry.register_thread(job_thread)
                        pin_task = threading.Thread(target=job_thread.run)
                        pin_task.daemon = True
                        pin_task.start()
                        return Response(status=200, mimetype='application/json')
                    case - 1:
                        ret__message = 'No response (' + input_token.pin_name + ').'
                        logger.debug(ret__message)
                        return Response(ret__message, status=404, mimetype='application/json')
                        pass
                    case - 2:
                        ret__message = 'Unauthorized (' + input_token.pin_name + ').'
                        logger.debug(ret__message)
                        return Response(ret__message, status=401, mimetype='application/json')
                        pass
                    case - 3:
                        ret__message = 'Invalid path (' + input_token.pin_name + ').'
                        logger.debug(ret__message)
                        return Response(ret__message, status=401, mimetype='application/json')
                        pass
                return Response(status=400, mimetype='application/json')
            except BaseException as e:
                logger.debug('Corrupted token: : ' + str(e))
                logger.debug(traceback.format_exc())
                return Response('Error of type ' + type(e).__name__ + ':' + str(e), status=200,
                                mimetype='application/json')
        except BaseException as e:
            logger.debug('Corrupted token: : ' + str(e))
            logger.debug(traceback.format_exc())
            return Response(str(e), status=400, mimetype='application/json')

    @app.route('/status', methods=['GET'])
    def get_status():
        return Response(json.dumps(snake_dict_to_camel_dict(__registry.get_job_status().__dict__)), status=200,
                        mimetype='application/json')

    return app
