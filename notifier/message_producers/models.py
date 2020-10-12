import json

import structlog

from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import ExternalMessage
from .producers.message_producer import PRODUCER_REGISTRY_NAME, MessageProducer

logger = structlog.get_logger(__name__)


class CustomProducer(ABCCustomObjectModel, MessageProducer):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME

    async def produce_messages(self) -> list[ExternalMessage]:
        process = await self._create_process()
        stdout, stderr = await process.communicate()
        exit_code = await process.wait()
        if stderr or exit_code != 0:
            raise Exception(f'Error: {stderr.decode()}, exit code: {exit_code}')

        raw_messages = json.loads(stdout.decode())
        return [ExternalMessage(**message) for message in raw_messages]


class ProducerModel(ABCObjectModel):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME
    CUSTOM_OBJECT_MODEL = CustomProducer
