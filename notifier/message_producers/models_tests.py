import pytest
import shutil
from django.conf import settings
import os
from .models import CustomProducer


@pytest.mark.asyncio
async def test_produce_messages() -> None:
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
    actual_messages = await custom_producer.produce_messages()
    expected_messages = [
        {'sender': 'user1', 'receiver': 'user2', 'content': 'content1'},
        {'sender': 'user2', 'receiver': 'user1', 'content': 'content2'},
    ]
    assert actual_messages == expected_messages
