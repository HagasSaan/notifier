import structlog
from django.db import models

from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import CONSUMER_REGISTRY_NAME
from helpers.registry import Registry

logger = structlog.get_logger(__name__)


class ConsumerModel(ABCObjectModel):
    DEFAULT_REGISTRY = Registry(CONSUMER_REGISTRY_NAME)

    object_type = models.CharField(
        max_length=100,
        choices=[
            (key, key)
            for key in DEFAULT_REGISTRY.keys
        ],
    )
