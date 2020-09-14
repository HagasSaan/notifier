import structlog
from django.db import models

from helpers.abc_object_model import ABCObjectModel
from helpers.registry import Registry
from .consumers.message_consumer import CONSUMER_REGISTRY_NAME

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
