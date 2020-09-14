import abc
from typing import List, Any, Dict

from . import Message
from ..registry import Registry

MESSAGE_FILTER_REGISTRY_NAME = 'MessageFilter'


class BaseMessageFilter(abc.ABC):
    def __call__(
        self,
        messages: List[Message],
        **kwargs: Dict[str, Any],
    ) -> List[Message]:
        ...


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class SkipKeywordsMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[Message],
        **kwargs: Dict[str, Any]
    ) -> List[Message]:
        pass
