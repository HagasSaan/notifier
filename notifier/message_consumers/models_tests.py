import os
import shutil

import pytest
from django.conf import settings

from helpers.messages_components import ExternalMessage
from .models import CustomConsumer


@pytest.mark.asyncio
async def test_consume_messages() -> None:
    filename = 'default/message_consumer.py'
    os.makedirs(f'{settings.MEDIA_ROOT}/default', exist_ok=True)
    shutil.copy(
        f'{os.path.dirname(__file__)}/test_fixtures/{filename}',
        f'{settings.MEDIA_ROOT}/{filename}',
    )
    custom_producer = CustomConsumer(
        executor=CustomConsumer.Executor.PYTHON,
        name='custom_producer_name',
        file=filename,
    )
    messages = [
        ExternalMessage(**{'sender': 'user1', 'receiver': 'user2', 'content': 'content1'}),
        ExternalMessage(**{'sender': 'user2', 'receiver': 'user1', 'content': 'content2'}),
    ]
    await custom_producer.consume_messages(messages)


@pytest.mark.asyncio
async def test_consume_messages_raises_error() -> None:
    filename = 'default/broken_message_consumer.py'
    os.makedirs(f'{settings.MEDIA_ROOT}/default', exist_ok=True)
    shutil.copy(
        f'{os.path.dirname(__file__)}/test_fixtures/{filename}',
        f'{settings.MEDIA_ROOT}/{filename}',
    )
    custom_producer = CustomConsumer(
        executor=CustomConsumer.Executor.PYTHON,
        name='custom_producer_name',
        file=filename,
    )
    with pytest.raises(
        Exception,
        match='Error: Internal error in script\n, exit code: 255'
    ):
        await custom_producer.consume_messages([])
