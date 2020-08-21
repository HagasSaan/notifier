from unittest.mock import MagicMock

import pytest
import telebot
from django.core.exceptions import ValidationError
from telebot.apihelper import ApiException
from telebot.types import Chat

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
    with pytest.raises(
        ValidationError,
        match='chat not found'
    ):
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
        TelegramGroupChat.validate_params(
            {
                'bot_token': 'fake:token',
                'chat_id': 123456789,
            }
        )
