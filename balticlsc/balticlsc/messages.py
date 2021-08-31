import enum


class SeqToken:
    seq_uid: str
    no: int
    is_final: bool


class InputTokenMessage:
    msg_uid: str
    pin_name: str
    access_type: str
    values: str


class Status(enum.Enum):
    IDLE = 0
    WORKING = 1
    COMPLETED = 2
    FAILED = 3
