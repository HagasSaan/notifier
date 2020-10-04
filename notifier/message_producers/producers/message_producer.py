import abc
from typing import List

from helpers.messages_components import ExternalMessage
from helpers.traits import Validatable


class MessageProducer(Validatable):
    USERNAME_KEY = 'undefined'

    @abc.abstractmethod
    async def produce_messages(self) -> List[ExternalMessage]:
        raise NotImplementedError


PRODUCER_REGISTRY_NAME = 'Producer'
