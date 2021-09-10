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

    def __init__(self):
        pass
