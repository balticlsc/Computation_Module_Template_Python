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
    token_seq_stack: []


class Status(enum.Enum):
    IDLE = 0
    WORKING = 1
    COMPLETED = 2
    FAILED = 3


class JobStatus:
    job_instance_uid: str
    job_progress: int
    status: Status


class OutputTokenMessage:
    pin_name: str
    values: str
    sender_uid: str
    required_msg_uid: str
    is_final: bool


class TokensAck:
    msg_uids: []
    sender_uid: str
    is_final: bool
    is_failed: bool
    note: str
