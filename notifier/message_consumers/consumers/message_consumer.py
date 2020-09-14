import abc
import dataclasses
from typing import List, Union, Dict

from django.forms import JSONField

from helpers.messages_components import Message


@dataclasses.dataclass
class MessageConsumer(abc.ABC):
    username_key = 'undefined'

    @abc.abstractmethod
    async def consume_messages(self, messages: List[Message]) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        raise NotImplementedError


CONSUMER_REGISTRY_NAME = 'Consumer'
