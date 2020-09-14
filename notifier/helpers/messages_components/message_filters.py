import abc
from typing import List

from . import Message


class AbstractMessageFilter(abc.ABC):
    @abc.abstractmethod
    def filter(self, messages: List[Message]):
        ...
