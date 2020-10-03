from typing import Dict, List

import structlog
from django.db import models

from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import ExternalMessage
from helpers.registry import Registry
from .producers.message_producer import PRODUCER_REGISTRY_NAME

logger = structlog.get_logger(__name__)


class CustomProducer(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='custom_producers')

    @property
    def __name__(self):
        return str(self)

    def __str__(self):
        return f'{self.name}: {self.file}'

    def save(self, **kwargs: Dict) -> None:
        super().save(**kwargs)
        get_all_custom_producers()

    async def produce_messages(self) -> List[ExternalMessage]:
        # TODO: run saved file, get List[Dict] with messages, and return it
        pass


def get_all_custom_producers() -> None:
    # TODO: может добавить фильтры того, что уже есть?
    #  а то не айс чёт
    #  еще вариант отображать конкретно добавленный кастомпродюсер
    _custom_producers = CustomProducer.objects.all()
    for producer in _custom_producers:
        Registry(PRODUCER_REGISTRY_NAME).set(producer, raise_if_exists=False)


class ProducerModel(ABCObjectModel):
    DEFAULT_REGISTRY = Registry(PRODUCER_REGISTRY_NAME)


get_all_custom_producers()
