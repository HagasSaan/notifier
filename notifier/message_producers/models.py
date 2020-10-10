import asyncio
import json
from typing import Union

import structlog
from django.db.models import JSONField
from django.conf import settings
from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import ExternalMessage
from .producers.message_producer import PRODUCER_REGISTRY_NAME, MessageProducer

logger = structlog.get_logger(__name__)


class CustomProducer(ABCCustomObjectModel, MessageProducer):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME

    async def produce_messages(self) -> list[ExternalMessage]:
        process = await asyncio.create_subprocess_exec(
            self.executor,
            f'{settings.MEDIA_ROOT}/{self.file.name}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        await process.wait()
        return json.loads(stdout.decode())

    @classmethod
    def validate_params(cls, params: Union[dict, JSONField]) -> None:
        pass


class ProducerModel(ABCObjectModel):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME
    CUSTOM_OBJECT_MODEL = CustomProducer
