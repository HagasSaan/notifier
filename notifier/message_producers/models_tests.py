import os
import shutil

import pytest
from django.conf import settings

from helpers.messages_components import ExternalMessage
from .models import CustomProducer


@pytest.mark.asyncio
async def test_produce_external_messages() -> None:
    filename = 'default/message_producer.py'
    os.makedirs(f'{settings.MEDIA_ROOT}/default', exist_ok=True)
    shutil.copy(
        f'{os.path.dirname(__file__)}/test_fixtures/{filename}',
        f'{settings.MEDIA_ROOT}/{filename}',
    )
    custom_producer = CustomProducer(
        executor=CustomProducer.Executor.PYTHON,
        name='custom_producer_name',
        file=filename,
    )
    actual_messages = await custom_producer.produce_external_messages()
    expected_messages = [
        ExternalMessage(**{'sender': 'user1', 'receiver': 'user2', 'content': 'content1'}),
        ExternalMessage(**{'sender': 'user2', 'receiver': 'user1', 'content': 'content2'}),
    ]
    assert actual_messages == expected_messages


@pytest.mark.asyncio
async def test_produce_external_messages_raises_error() -> None:
    filename = 'default/broken_message_producer.py'
    os.makedirs(f'{settings.MEDIA_ROOT}/default', exist_ok=True)
    shutil.copy(
        f'{os.path.dirname(__file__)}/test_fixtures/{filename}',
        f'{settings.MEDIA_ROOT}/{filename}',
    )
    custom_producer = CustomProducer(
        executor=CustomProducer.Executor.PYTHON,
        name='custom_producer_name',
        file=filename,
    )
    with pytest.raises(
        Exception,
        match='Error: Internal error in script\n, exit code: 255',
    ):
        await custom_producer.produce_external_messages()
