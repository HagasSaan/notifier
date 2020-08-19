import abc
import dataclasses
from typing import Any, List, Union, Dict

from django.db.models import JSONField


@dataclasses.dataclass
class Message:
    # TODO: Replace User in typings with user from Configs
    sender: Union[str, 'User']
    receiver: Union[str, 'User']
    content: Any


class CanProduceMessages(abc.ABC):

    @property
    @abc.abstractmethod
    def username_key(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def produce_messages(self) -> List[Message]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def validate_params(cls, params: Union[Dict, JSONField]):
        raise NotImplementedError


PRODUCER_REGISTRY_NAME = 'Producer'


class CanConsumeMessages(abc.ABC):

    @property
    @abc.abstractmethod
    def username_key(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def consume_messages(self, messages: List[Message]):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def validate_params(cls, params: Union[Dict, JSONField]):
        raise NotImplementedError


CONSUMER_REGISTRY_NAME = 'Consumer'
