import abc
from typing import List

from . import Message


class AbstractMessageFilter(abc.ABC):
    @abc.abstractmethod
    def __call__(self, messages: List[Message], *args, **kwargs) -> List[Message]:
        ...
