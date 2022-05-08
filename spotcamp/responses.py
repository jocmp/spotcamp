from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, TypeVar
from xmlrpc.client import Boolean

T = TypeVar('T')


class Status(Enum):
    SUCCESS = 1
    FAILURE = 2


@dataclass
class Response(Generic[T]):
    value: T
    errors: Any
    status: Status

    @staticmethod
    def success(value: T):
        return Response(value=value, errors=None, status=Status.SUCCESS)

    @staticmethod
    def failure(value: T = None):
        return Response(value=value, errors=None, status=Status.FAILURE)

    def is_failure(self) -> Boolean:
        return self.status == Status.FAILURE
