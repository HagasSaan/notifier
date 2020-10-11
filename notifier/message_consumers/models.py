import asyncio
import dataclasses
import json
from typing import Union

import structlog
from django.conf import settings
from django.db.models import JSONField

from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import ExternalMessage
from .consumers.message_consumer import CONSUMER_REGISTRY_NAME, MessageConsumer

logger = structlog.get_logger(__name__)


class CustomConsumer(ABCCustomObjectModel, MessageConsumer):
    REGISTRY_NAME = CONSUMER_REGISTRY_NAME

    async def consume_messages(self, messages: list[ExternalMessage]) -> None:
        messages = [dataclasses.asdict(message) for message in messages]
        raw_messages = json.dumps(messages).encode()
        process = await asyncio.create_subprocess_exec(
            self.executor,
            f'{settings.MEDIA_ROOT}/{self.file.name}',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate(raw_messages)
        exit_code = await process.wait()
        if stderr:
            raise Exception(f'Error: {stderr}, exit code: {exit_code}')

    @classmethod
    def validate_params(cls, params: Union[dict, JSONField]) -> None:
        pass


class ConsumerModel(ABCObjectModel):
    REGISTRY_NAME = CONSUMER_REGISTRY_NAME
    CUSTOM_OBJECT_MODEL = CustomConsumer
