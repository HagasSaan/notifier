import dataclasses
from typing import Union

import factory
from django.db.models import JSONField

from helpers.messages_components import ExternalMessage
from helpers.registry import Registry
from . import models
from .producers.message_producer import PRODUCER_REGISTRY_NAME, MessageProducer


@Registry.register(PRODUCER_REGISTRY_NAME)
@dataclasses.dataclass
class SampleProducer(MessageProducer):
    field_1: str
    field_2: int

    USERNAME_KEY = 'test_producer'

    async def produce_messages(self) -> list[ExternalMessage]:
        pass

    @classmethod
    def validate_params(cls, params: Union[dict, JSONField]) -> None:
        pass


class ProducerModelFactory(factory.django.DjangoModelFactory):
    name = f'producer_model_{SampleProducer.__name__}'
    object_type = SampleProducer.__name__
    parameters = {
        name: type_(1234)
        for (name, type_) in SampleProducer.__annotations__.items()
    }

    class Meta:
        model = models.ProducerModel
