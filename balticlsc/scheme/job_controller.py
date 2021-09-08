from typing import Type
from flask import Flask
from balticlsc.scheme.job_thread import TokenListener


def init_job_controller(listener: Type[TokenListener]) -> Flask:
    pass
