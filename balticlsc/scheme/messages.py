from enum import Enum


class SeqToken:
    seq_uid: str
    no: int
    is_final: bool

    def __init__(self, seq_uid: str, no: int, is_final: bool):
        self.seq_uid = seq_uid
        self.no = no
        self.is_final = is_final


class InputTokenMessage:
    msg_uid: str
    pin_name: str
    values: str
    access_type: str
    token_seq_stack: []

    def __init__(self, msg_uid: str, pin_name: str, values: str, access_type: str, token_seq_stack: []):
        self.msg_uid = msg_uid
        self.pin_name = pin_name
        self.values = values
        self.access_type = access_type
        self.token_seq_stack = token_seq_stack


class Status(Enum):
    IDLE = 0
    WORKING = 1
    COMPLETED = 2
    FAILED = 3


class JobStatus:
    job_instance_uid: str
    status: Status
    job_progress: int

    def __init__(self, job_instance_uid: str, status: Status = Status.IDLE, job_progress: int = -1):
        self.job_instance_uid = job_instance_uid
        self.job_progress = job_progress
        self.status = status


class OutputTokenMessage:
    pin_name: str
    sender_uid: str
    values: str
    base_msg_uid: str
    is_final: bool

    def __init__(self, pin_name: str, sender_uid: str, values: str, base_msg_uid: str, is_final: bool):
        self.pin_name = pin_name
        self.sender_uid = sender_uid
        self.values = values
        self.base_msg_uid = base_msg_uid
        self.is_final = is_final


class TokensAck:
    sender_uid: str
    msg_uids: []
    note: str
    is_final: bool
    is_failed: bool

    def __init__(self, sender_uid: str, msg_ids: [], note: str, is_final: bool, is_failed: bool):
        self.sender_uid = sender_uid
        self.msg_uids = msg_ids
        self.note = note
        self.is_final = is_final
        self.is_failed = is_failed
