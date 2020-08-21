from unittest.mock import MagicMock

import pytest
import telebot
from django.core.exceptions import ValidationError
from telebot.apihelper import ApiException
from telebot.types import Chat

from helpers.messages_components import Message
from .telegram import TelegramGroupChat


def test_validate_params(mocker):
    chat_id = 123456

    patched_telebot = MagicMock()
    mocker.patch.object(telebot, 'AsyncTeleBot', return_value=patched_telebot)
    mocked_chat = MagicMock()
    patched_telebot.get_chat.return_value = mocked_chat
    mocked_chat.wait.return_value = Chat(chat_id, None)
    TelegramGroupChat.validate_params(
        {
            'bot_token': 'fake:token',
            'chat_id': chat_id,
        }
    )


def test_validate_params_should_raise_validation_error(mocker):
    patched_telebot = MagicMock()
    mocker.patch.object(telebot, 'AsyncTeleBot', return_value=patched_telebot)
    mocked_chat = MagicMock()
    patched_telebot.get_chat.return_value = mocked_chat
    mocked_chat.wait.return_value = (
        ApiException,
        ApiException(
            'A request to the Telegram API was unsuccessful. '
            'The server returned HTTP 400 Bad Request. Response body: '
            '[b\'{"ok":false,"error_code":400,"description":"Bad Request: chat not found"}\']',
            None, None,
        ),
        'traceback'
    )

    with pytest.raises(
        ValidationError,
        match=TelegramGroupChat.CHAT_NOT_FOUND
    ):
        TelegramGroupChat.validate_params(
            {
                'bot_token': 'fake:token',
                'chat_id': 123456789,
            }
        )


@pytest.mark.asyncio
async def test_send_message(mocker):
    chat_id = 123456
    message = Message(
        sender='@sender',
        receiver='@receiver',
        content='testing message',
    )

    patched_telebot = MagicMock()
    mocker.patch.object(telebot, 'AsyncTeleBot', return_value=patched_telebot)

    bot = TelegramGroupChat(
        bot_token='fake:token',
        chat_id=chat_id
    )
    await bot.send_message(message)

    patched_telebot.send_message.assert_called_once_with(
        chat_id, f'From {message.sender} to {message.receiver}: {message.content}'
    )


@pytest.mark.asyncio
async def test_send_message_raises_validation_error(mocker):
    chat_id = 123
    message = Message(
        sender='@sender',
        receiver='@receiver',
        content='testing mhagassaanessage',
    )

    patched_telebot = MagicMock()
    mocker.patch.object(telebot, 'AsyncTeleBot', return_value=patched_telebot)
    mocked_send_message = MagicMock()
    patched_telebot.send_message.return_value = mocked_send_message
    mocked_send_message.wait.return_value = (
        ApiException,
        ApiException(
            'A request to the Telegram API was unsuccessful. '
            'The server returned HTTP 400 Bad Request. Response body: '
            '[b\'{"ok":false,"error_code":400,"description":"Bad Request: chat not found"}\']',
            None, None,
        ),
        'traceback',
    )

    bot = TelegramGroupChat(
        bot_token='fake:token',
        chat_id=chat_id
    )
    with pytest.raises(
        ValidationError,
        match=TelegramGroupChat.CHAT_NOT_FOUND,
    ):
        await bot.send_message(message)
