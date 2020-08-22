import structlog
from django.db import models

from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import PRODUCER_REGISTRY_NAME
from helpers.registry import Registry

logger = structlog.get_logger(__name__)


class ProducerModel(ABCObjectModel):
    DEFAULT_REGISTRY = Registry(PRODUCER_REGISTRY_NAME)
    object_type = models.CharField(
        max_length=100,
        choices=[
            (key, key)
            for key in DEFAULT_REGISTRY.keys
        ],
    )
