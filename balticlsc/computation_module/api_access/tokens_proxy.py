import json
import os
from http import HTTPStatus
import requests
from balticlsc.computation_module.data_model.messages import OutputTokenMessage, TokensAck
from balticlsc.computation_module.utils.utils import snake_dict_to_camel_dict


class TokensProxy:

    def __init__(self):
        self.__sender_uid = os.getenv('SYS_MODULE_INSTANCE_UID', 'module_uid')
        self.__batch_manager_ack_url = os.getenv('SYS_BATCH_MANAGER_ACK_ENDPOINT', 'http://127.0.0.1:7000/ack')
        self.__batch_manager_token_url = os.getenv('SYS_BATCH_MANAGER_TOKEN_ENDPOINT', 'http://127.0.0.1:7000/token')

    def send_output_token(self, pin_name: str, values: str, msg_id: str, is_final: bool) -> HTTPStatus:
        output_token = OutputTokenMessage(pin_name, self._TokensProxy__sender_uid, values, msg_id, is_final)
        return HTTPStatus(requests.post(self._TokensProxy__batch_manager_token_url,
                                        data=json.dumps(snake_dict_to_camel_dict(output_token.__dict__)),
                                        headers={'module-type': 'application/json'}).status_code)

    def send_ack_token(self, msg_ids: [], is_final: bool, is_failed: bool = False, note: str = None) -> HTTPStatus:
        ack_token = TokensAck(self.__sender_uid, msg_ids, note, is_final, is_failed)
        return HTTPStatus(requests.post(self._TokensProxy__batch_manager_ack_url,
                                        data=json.dumps(snake_dict_to_camel_dict(ack_token.__dict__)),
                                        headers={'module-type': 'application/json'}).status_code)
