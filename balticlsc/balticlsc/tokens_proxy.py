from http import HTTPStatus


class TokensProxy:

    def send_output_token(self, pin_name: str, values: str, msg_uid: str, is_final: bool) -> HTTPStatus:
        pass

    def send_ack_token(self, msg_ids: [], is_final: bool, is_failed: bool = False, note: str = None):
        pass
