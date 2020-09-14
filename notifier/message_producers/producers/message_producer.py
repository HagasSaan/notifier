import abc
import dataclasses
from typing import List

from helpers.messages_components import Message


@dataclasses.dataclass
class MessageProducer(abc.ABC):
    username_key = 'undefined'

    @abc.abstractmethod
    async def produce_messages(self) -> List[Message]:
        raise NotImplementedError


PRODUCER_REGISTRY_NAME = 'Producer'
