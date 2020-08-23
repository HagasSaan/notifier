import dataclasses
from typing import List, Any, Dict

from helpers.messages_components import CONSUMER_REGISTRY_NAME, Message
from helpers.registry import Registry
from .chats_base import Chat


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class GoogleChat(Chat):
    username_key = 'google_username'

    async def consume_messages(self, messages: List[Message]) -> None:
        pass

    async def send_message(
        self,
        message: Message,
        *args: List[Any],
        **kwargs: Dict[Any, Any],
    ) -> None:
        raise NotImplementedError
