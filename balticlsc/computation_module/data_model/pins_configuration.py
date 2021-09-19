import json
import os
from enum import Enum
from balticlsc.computation_module.utils.utils import camel_dict_to_snake_dict


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
    access_credential: {}

    def __init__(self, pin_name: str, pin_type: str, is_required: str, token_multiplicity: Multiplicity,
                 data_multiplicity: Multiplicity, access_type: str, access_credential: {}):
        self.pin_name = pin_name
        self.pin_type = pin_type
        self.is_required = is_required
        self.token_multiplicity = token_multiplicity
        self.data_multiplicity = data_multiplicity
        self.access_type = access_type
        self.access_credential = access_credential


def get_pins_configuration() -> []:
    pins_config_path = os.getenv('SYS_PIN_CONFIG_FILE_PATH', '/app/module/configs/pins.json')
    with open(pins_config_path) as pins_config_file:
        try:
            pins_configuration = []
            for p in json.load(pins_config_file):
                try:
                    pin = PinConfiguration(
                        **{key: Multiplicity[value.upper()] if key in ('token_multiplicity',
                                                                       'data_multiplicity') else value
                           for key, value in camel_dict_to_snake_dict(p).items()
                           if key in PinConfiguration.__dict__['__annotations__']})
                except BaseException as lpe:
                    error_msg = 'Wrong config for pin - json:' + str(p) + ', error: ' + str(lpe)
                    raise ValueError(error_msg) from lpe
                pins_configuration.append(pin)
        except BaseException as lpe:
            error_msg = 'Error while loading pins config from ' + pins_config_path + ': ' + str(lpe)
            raise ValueError(error_msg) from lpe
    return pins_configuration
