from typing import List

import structlog

from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import ExternalMessage
from helpers.registry import Registry
from .producers.message_producer import PRODUCER_REGISTRY_NAME

logger = structlog.get_logger(__name__)


class CustomProducer(ABCCustomObjectModel):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME

    async def produce_messages(self) -> List[ExternalMessage]:
        pass


class ProducerModel(ABCObjectModel):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME
    CUSTOM_OBJECT_MODEL = CustomProducer


Registry(PRODUCER_REGISTRY_NAME).subscribe(ProducerModel)
CustomProducer.get_all_custom_objects()
