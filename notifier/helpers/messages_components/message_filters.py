import abc
import dataclasses
from typing import List, Any, Dict, Union

from django.forms import JSONField

from . import Message
from ..registry import Registry

MESSAGE_FILTER_REGISTRY_NAME = 'MessageFilter'


class BaseMessageFilter(abc.ABC):
    def __call__(
        self,
        messages: List[Message],
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> List[Message]:
        ...

    # TODO: remove that stub when abc_object_model stops check everything
    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        pass


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class SkipKeywordsMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[Message],
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> List[Message]:
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
        messages: List[Message],
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> List[Message]:
        return [
            message
            for message in messages
            if message.receiver in kwargs['users']
        ]


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class ReceiverWorkingMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: List[Message],
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> List[Message]:
        return [
            message
            for message in messages
            if message.receiver.is_working_time
        ]
