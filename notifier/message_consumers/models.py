from typing import List

import structlog

from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import ExternalMessage
from .consumers.message_consumer import CONSUMER_REGISTRY_NAME

logger = structlog.get_logger(__name__)


class CustomConsumer(ABCCustomObjectModel):
    REGISTRY_NAME = CONSUMER_REGISTRY_NAME

    async def consume_messages(self, messages: List[ExternalMessage]) -> None:
        pass


class ConsumerModel(ABCObjectModel):
    REGISTRY_NAME = CONSUMER_REGISTRY_NAME
    CUSTOM_OBJECT_MODEL = CustomConsumer
