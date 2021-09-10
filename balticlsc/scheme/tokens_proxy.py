import os
from http import HTTPStatus
from balticlsc.scheme.messages import OutputTokenMessage, TokensAck


class TokensProxy:

    def __init__(self):
        self.__sender_uid = os.getenv('SYS_MODULE_INSTANCE_UID', 'module_uid')
        self.__batch_manager_ack_url = os.getenv('SYS_BATCH_MANAGER_ACK_ENDPOINT', 'http://127.0.0.1:7000/ack')
        self.__batch_manager_token_url = os.getenv('SYS_BATCH_MANAGER_TOKEN_ENDPOINT', 'http://127.0.0.1:7000/token')

    def send_output_token(self, pin_name: str, values: str, msg_uid: str, is_final: bool) -> HTTPStatus:
        output_token = OutputTokenMessage()
        pass

    def send_ack_token(self, msg_ids: [], is_final: bool, is_failed: bool = False, note: str = None) -> HTTPStatus:
        ack_token = TokensAck()
        pass
