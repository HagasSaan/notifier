import abc
from typing import List, Any, Dict

from . import InternalMessage
from ..registry import Registry

MESSAGE_FILTER_REGISTRY_NAME = 'MessageFilter'


class BaseMessageFilter(abc.ABC):
    def __call__(
        self,
        messages: List[InternalMessage],
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> List[InternalMessage]:
        ...


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class SkipKeywordsMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[InternalMessage],
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> List[InternalMessage]:
        return [
            message
            for message in messages
            if not any(
                skip_keyword in message.content
                for skip_keyword in kwargs['skip_keywords']
            )
        ]


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class ReceiverExistsMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[InternalMessage],
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> List[InternalMessage]:
        return [
            message
            for message in messages
            if message.receiver in kwargs['users']
        ]


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class ReceiverWorkingMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[InternalMessage],
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> List[InternalMessage]:
        return [
            message
            for message in messages
            if message.receiver.is_working_time
        ]
