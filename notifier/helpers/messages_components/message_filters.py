import abc
from typing import Union, Any

from django.db.models import JSONField

from . import InternalMessage
from ..registry import Registry
from ..traits import Validatable

MESSAGE_FILTER_REGISTRY_NAME = 'MessageFilter'


class BaseMessageFilter(abc.ABC):
    def __init__(self, **kwargs: dict):
        ...

    def __call__(
        self,
        messages: list[InternalMessage],
        configuration: 'Configuration',  # noqa F821
    ) -> list[InternalMessage]:
        ...


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class SkipKeywordsMessageFilter(BaseMessageFilter, Validatable):
    skip_keywords: list[str]

    def __init__(self, **kwargs: dict[str, Any]):
        super().__init__(**kwargs)
        self.skip_keywords = kwargs['skip_keywords']

    def __call__(
        self,
        messages: list[InternalMessage],
        configuration: 'Configuration',  # noqa F821
    ) -> list[InternalMessage]:
        return [
            message
            for message in messages
            if not any(
                skip_keyword in message.content
                for skip_keyword in self.skip_keywords
            )
        ]

    @classmethod
    def validate_params(cls, params: Union[dict, JSONField]) -> None:
        _ = params['skip_keywords']


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class ReceiverExistsMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: list[InternalMessage],
        configuration: 'Configuration',  # noqa F821
    ) -> list[InternalMessage]:
        return [
            message
            for message in messages
            if message.receiver in configuration.users.all()
        ]


@Registry.register(MESSAGE_FILTER_REGISTRY_NAME)
class ReceiverWorkingMessageFilter(BaseMessageFilter):
    def __call__(
        self,
        messages: list[InternalMessage],
        configuration: 'Configuration',  # noqa F821
    ) -> list[InternalMessage]:
        return [
            message
            for message in messages
            if message.receiver.is_working_time
        ]
