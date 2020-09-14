import abc
import dataclasses
from typing import List, Union, Dict

from django.db.models import JSONField

from helpers.messages_components import Message


@dataclasses.dataclass
class MessageConsumer(abc.ABC):
    username_key = 'undefined'

    @abc.abstractmethod
    async def consume_messages(self, messages: List[Message]) -> None:
        raise NotImplementedError


CONSUMER_REGISTRY_NAME = 'Consumer'
