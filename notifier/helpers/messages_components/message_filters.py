import abc
from typing import List, Any, Dict

from configuration.models import Configuration
from . import InternalMessage
from ..registry import Registry

MESSAGE_FILTER_REGISTRY_NAME = 'MessageFilter'


class BaseMessageFilter(abc.ABC):
    def __call__(
        self,
        messages: List[InternalMessage],
        configuration: Configuration,
    ) -> List[InternalMessage]:
        ...


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class SkipKeywordsMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[InternalMessage],
        configuration: Configuration,
    ) -> List[InternalMessage]:
        return [
            message
            for message in messages
            if not any(
                skip_keyword in message.content
                for skip_keyword in configuration.skip_keywords_list
            )
        ]


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class ReceiverExistsMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[InternalMessage],
        configuration: Configuration,
    ) -> List[InternalMessage]:
        return [
            message
            for message in messages
            if message.receiver in configuration.users.all()
        ]


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class ReceiverWorkingMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[InternalMessage],
        configuration: Configuration,
    ) -> List[InternalMessage]:
        return [
            message
            for message in messages
            if message.receiver.is_working_time
        ]
