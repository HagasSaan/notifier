import abc
from typing import List

from helpers.messages_components import ExternalMessage
from helpers.traits import Validatable


class MessageConsumer(Validatable, abc.ABC):
    username_key = 'undefined'

    @abc.abstractmethod
    async def consume_messages(self, messages: List[ExternalMessage]) -> None:
        raise NotImplementedError


CONSUMER_REGISTRY_NAME = 'Consumer'
