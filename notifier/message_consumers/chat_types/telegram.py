import asyncio
import dataclasses
import telebot
from typing import List, Union, Dict

from django.core.exceptions import ValidationError
from django.db.models import JSONField
from telebot.util import AsyncTask

from helpers.messages_components import Message, CONSUMER_REGISTRY_NAME
from helpers.registry import Registry
from .chats_base import Chat


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class TelegramGroupChat(Chat):
    bot_token: str
    chat_id: int

    CHAT_NOT_FOUND = 'chat not found'

    @property
    def username_key(self):
        return 'telegram_username'

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]):
        bot = telebot.AsyncTeleBot(token=params['bot_token'])
        chat_task: AsyncTask = bot.get_chat(params['chat_id'])
        chat = chat_task.wait()
        if not isinstance(chat, telebot.types.Chat):
            exception = chat[1]
            if cls.CHAT_NOT_FOUND in str(exception):
                raise ValidationError(cls.CHAT_NOT_FOUND)

            raise exception

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
