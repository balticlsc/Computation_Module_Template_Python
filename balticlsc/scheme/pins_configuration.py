from enum import Enum


class Multiplicity(Enum):
    SINGLE = 0
    MULTIPLE = 1


class PinConfiguration:
    pin_name: str
    pin_type: str
    is_required: str
    token_multiplicity: Multiplicity
    data_multiplicity: Multiplicity
    access_type: str
    access_credential: str

    def __init__(self, pin_name: str, pin_type: str, is_required: str, token_multiplicity: Multiplicity,
                 data_multiplicity: Multiplicity, access_type: str, access_credential: str):
        self.pin_name = pin_name
        self.pin_type = pin_type
        self.is_required = is_required
        self.token_multiplicity = token_multiplicity
        self.data_multiplicity = data_multiplicity
        self.access_type = access_type
        self.access_credential = access_credential
