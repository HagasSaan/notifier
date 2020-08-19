import asyncio
import dataclasses
from typing import List, Union, Dict

from django.db.models import JSONField

from helpers.messages_components import Message, CONSUMER_REGISTRY_NAME
from helpers.registry import Registry
from .chats_base import Chat


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class TelegramGroupChat(Chat):

    @property
    def username_key(self):
        return 'telegram_username'

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]):
        pass

    async def consume_messages(self, messages: List[Message]):
        await asyncio.gather(
            *[
                self.send_message(
                    sender=message.sender,
                    receiver=message.receiver,
                    content=message.content,
                )
                for message in messages
            ]
        )

    async def send_message(self, *args, **kwargs):
        message = (
            f'From {kwargs["sender"]} '
            f'to {kwargs["receiver"]}: '
            f'{kwargs["content"]}'
        )
        await asyncio.sleep(1)
        # await self._bot.send_message(self.group_chat_id, message)


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class TelegramChat(Chat):

    @property
    def username_key(self):
        return 'telegram_user_chat_id'

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]):
        pass

    async def consume_messages(self, messages: List[Message]):
        pass

    async def send_message(self, *args, **kwargs):
        raise NotImplementedError
