from unittest.mock import MagicMock, call

import pytest
import telebot
from django.core.exceptions import ValidationError
from telebot.apihelper import ApiException
import telebot.types as tb_types

from helpers.messages_components import Message
from .telegram import TelegramGroupChat


@pytest.fixture
def m_telebot(mocker):
    patched_telebot = MagicMock()
    mocker.patch.object(telebot, 'AsyncTeleBot', return_value=patched_telebot)
    return patched_telebot


def test_validate_params(m_telebot):
    chat_id = 123456

    mocked_chat = MagicMock()
    m_telebot.get_chat.return_value = mocked_chat
    mocked_chat.wait.return_value = tb_types.Chat(chat_id, None)
    TelegramGroupChat.validate_params(
        {
            'bot_token': 'fake:token',
            'chat_id': chat_id,
        }
    )


def test_validate_params_should_raise_validation_error(m_telebot):
    mocked_chat = MagicMock()
    m_telebot.get_chat.return_value = mocked_chat
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
async def test_send_message(m_telebot):
    chat_id = 123456
    message = Message(
        sender='@sender',
        receiver='@receiver',
        content='testing message',
    )

    mocked_send_message = MagicMock()
    m_telebot.send_message.return_value = mocked_send_message
    mocked_send_message.wait.return_value = tb_types.Message(
        None, None, None, None, None, [], None
    )

    bot = TelegramGroupChat(
        bot_token='fake:token',
        chat_id=chat_id
    )
    await bot.send_message(message)

    m_telebot.send_message.assert_called_once_with(
        chat_id, f'From {message.sender} to {message.receiver}: {message.content}'
    )


@pytest.mark.asyncio
async def test_send_message_raises_validation_error(m_telebot):
    chat_id = 123
    message = Message(
        sender='@sender',
        receiver='@receiver',
        content='testing mhagassaanessage',
    )

    mocked_send_message = MagicMock()
    m_telebot.send_message.return_value = mocked_send_message
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


@pytest.mark.asyncio
async def test_consume_messages(m_telebot):
    chat_id = 123456
    messages = [
        Message(
            sender='@sender2',
            receiver='@receiver1',
            content='testing message 1',
        ),
        Message(
            sender='@sender1',
            receiver='@receiver2',
            content='testing message 2',
        ),
    ]

    mocked_send_message = MagicMock()
    m_telebot.send_message.return_value = mocked_send_message
    mocked_send_message.wait.return_value = tb_types.Message(
        None, None, None, None, None, [], None
    )

    bot = TelegramGroupChat(
        bot_token='fake:token',
        chat_id=chat_id
    )
    await bot.consume_messages(messages)

    m_telebot.send_message.assert_has_calls(
        [
            call(chat_id, f'From {messages[0].sender} to {messages[0].receiver}: {messages[0].content}'),
            call(chat_id, f'From {messages[1].sender} to {messages[1].receiver}: {messages[1].content}'),
        ],
        any_order=True,
    )
