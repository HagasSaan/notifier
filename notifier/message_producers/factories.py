import dataclasses
from typing import Union, Dict, List

import factory
from django.db.models import JSONField

from helpers.messages_components import MessageProducer, Message, PRODUCER_REGISTRY_NAME
from helpers.registry import Registry
from . import models


@Registry.register(PRODUCER_REGISTRY_NAME)
@dataclasses.dataclass
class TestProducer(MessageProducer):
    field_1: str
    field_2: int

    username_key = 'test_producer'

    async def produce_messages(self) -> List[Message]:
        pass

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        pass


class ProducerModelFactory(factory.django.DjangoModelFactory):
    name = f'producer_model_{TestProducer.__name__}'
    object_type = TestProducer.__name__
    parameters = {
        name: type_(1234)
        for (name, type_) in TestProducer.__annotations__.items()
    }

    class Meta:
        model = models.ProducerModel
