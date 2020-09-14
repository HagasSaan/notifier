import asyncio
import dataclasses
import traceback
from typing import List, Union, Dict, Tuple, Type, Any

import telebot
from django.core.exceptions import ValidationError
from django.db.models import JSONField
from telebot.util import AsyncTask

from helpers.registry import Registry
from ..message_consumer import CONSUMER_REGISTRY_NAME, Message, MessageConsumer


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class TelegramGroupChat(MessageConsumer):
    bot_token: str
    chat_id: int

    username_key = 'telegram_username'

    CHAT_NOT_FOUND = 'chat not found'

    def __post_init__(self):
        self._bot = telebot.AsyncTeleBot(self.bot_token)

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        bot = telebot.AsyncTeleBot(token=params['bot_token'])
        chat_task: AsyncTask = bot.get_chat(params['chat_id'])
        result = chat_task.wait()
        if not isinstance(result, telebot.types.Chat):
            cls._handle_error(result)

    async def consume_messages(self, messages: List[Message]) -> None:
        await asyncio.gather(
            *[
                self.send_message(message)
                for message in messages
            ],
            return_exceptions=True,
        )
        # TODO: Handle exceptions

    async def send_message(
        self,
        message: Message,
        *args: List[Any],
        **kwargs: Dict[Any, Any],
    ) -> None:
        message_text = f'From {message.sender} to {message.receiver}: {message.content}'
        send_message_task: AsyncTask = self._bot.send_message(self.chat_id, message_text)
        result = send_message_task.wait()
        if not isinstance(result, telebot.types.Message):
            self._handle_error(result)

    @classmethod
    def _handle_error(
        cls,
        error: Tuple[Type[Exception], Exception, traceback.TracebackException],
    ) -> None:
        _, exception, _ = error
        if cls.CHAT_NOT_FOUND in str(exception):
            raise ValidationError(cls.CHAT_NOT_FOUND)

        raise exception


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class TelegramChat(MessageConsumer):
    username_key = 'telegram_user_chat_id'

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        pass

    async def consume_messages(self, messages: List[Message]) -> None:
        pass

    async def send_message(
        self,
        message: Message,
        *args: List[Any],
        **kwargs: Dict[Any, Any],
    ) -> None:
        raise NotImplementedError
