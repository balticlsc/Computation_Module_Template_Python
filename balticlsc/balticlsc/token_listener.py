class TokenListener:
    pass


class MyTokenListener:

    def optional_data_received(self, pin_name: str):
        pass

    def data_received(self, pin_name: str):
        pass

    def data_ready(self):
        pass

    def data_complete(self):
        pass
