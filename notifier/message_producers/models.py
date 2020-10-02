from typing import Dict

import structlog
from django.db import models

from helpers.abc_object_model import ABCObjectModel
from helpers.registry import Registry
from .producers.message_producer import PRODUCER_REGISTRY_NAME

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


class CustomProducer(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='custom_producers')

    def __str__(self):
        return f'{self.name}: {self.file}'

    def save(self, **kwargs: Dict) -> None:
        super().save(**kwargs)
