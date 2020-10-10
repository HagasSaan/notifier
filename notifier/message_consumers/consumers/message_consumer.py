import abc

from helpers.messages_components import ExternalMessage
from helpers.traits import Validatable


class MessageConsumer(Validatable):
    USERNAME_KEY = 'undefined'

    @abc.abstractmethod
    async def consume_messages(self, messages: list[ExternalMessage]) -> None:
        raise NotImplementedError


CONSUMER_REGISTRY_NAME = 'Consumer'
