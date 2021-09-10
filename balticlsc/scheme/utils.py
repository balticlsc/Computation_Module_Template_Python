import re
from enum import Enum


def camel_dict_to_snake_dict(source: {}) -> {}:
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return {pattern.sub('_', key).lower(): list(camel_dict_to_snake_dict(in_value) for in_value in value
                                                ) if isinstance(value, type([])) else value for key, value
            in source.items()}


def snake_dict_to_camel_dict(source: {}) -> {}:
    return {''.join(word.title() for word in key.split('_')): value.name.title() if isinstance(value, Enum) else value
            for key, value in source.items()}
