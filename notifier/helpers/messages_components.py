import abc
import dataclasses
from typing import List, Union, Dict, Any

from django.db.models import JSONField


@dataclasses.dataclass
class Message:
    # TODO: get normal typing from config user
    sender: Union[str, 'User']  # noqa F821
    receiver: Union[str, 'User']  # noqa F821
    content: Any

    def __hash__(self):
        # TODO: do it in cycle, cuz new field can be added
        return (
            hash(self.sender)
            + hash(self.receiver)
            + hash(self.content)
        )


@dataclasses.dataclass
class MessageProducer(abc.ABC):
    username_key = 'undefined'

    @abc.abstractmethod
    async def produce_messages(self) -> List[Message]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        raise NotImplementedError


PRODUCER_REGISTRY_NAME = 'Producer'


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
