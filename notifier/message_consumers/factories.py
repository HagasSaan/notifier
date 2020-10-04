import dataclasses
from typing import Union, Dict, List

import factory
from django.db.models import JSONField

from helpers.messages_components import ExternalMessage
from helpers.registry import Registry
from . import models
from .consumers.message_consumer import CONSUMER_REGISTRY_NAME, MessageConsumer


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class SampleConsumer(MessageConsumer):
    field_1: str
    field_2: int

    USERNAME_KEY = 'test_consumer'

    async def consume_messages(self, messages: List[ExternalMessage]) -> None:
        pass

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        pass


class ConsumerModelFactory(factory.django.DjangoModelFactory):
    name = f'consumer_model_{SampleConsumer.__name__}'
    object_type = SampleConsumer.__name__
    parameters = {
        name: type_(1234)
        for (name, type_) in SampleConsumer.__annotations__.items()
    }

    class Meta:
        model = models.ConsumerModel
