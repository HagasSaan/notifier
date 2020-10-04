from typing import List, Union, Dict

import structlog
from django.db.models import JSONField

from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import ExternalMessage
from .producers.message_producer import PRODUCER_REGISTRY_NAME, MessageProducer

logger = structlog.get_logger(__name__)


class CustomProducer(ABCCustomObjectModel, MessageProducer):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME

    async def produce_messages(self) -> List[ExternalMessage]:
        return []

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        pass


class ProducerModel(ABCObjectModel):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME
    CUSTOM_OBJECT_MODEL = CustomProducer
