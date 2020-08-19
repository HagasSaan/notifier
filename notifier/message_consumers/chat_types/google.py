import dataclasses
from typing import List

from helpers.messages_components import CONSUMER_REGISTRY_NAME, Message
from helpers.registry import Registry
from .chats_base import Chat


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class GoogleChat(Chat):

    @property
    def username_key(self):
        return 'google_username'

    async def consume_messages(self, messages: List[Message]):
        pass

    async def send_message(self, *args, **kwargs):
        raise NotImplementedError
