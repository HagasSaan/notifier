import abc
from typing import List, Any, Dict

from . import Message


class AbstractMessageFilter(abc.ABC):
    @abc.abstractmethod
    def __call__(
        self,
        messages: List[Message],
        **kwargs: Dict[str, Any],
    ) -> List[Message]:
        ...
