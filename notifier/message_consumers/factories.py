import dataclasses
from typing import Union, Dict, List

import factory
from django.db.models import JSONField

from helpers.messages_components import MessageConsumer, Message, CONSUMER_REGISTRY_NAME
from helpers.registry import Registry
from . import models


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class TestConsumer(MessageConsumer):
    field_1: str
    field_2: int

    @property
    def username_key(self) -> str:
        return 'test_consumer'

    async def consume_messages(self, messages: List[Message]) -> None:
        pass

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        pass


class ConsumerModelFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'consumer_model_{n}')
    object_type = factory.Sequence(lambda _: TestConsumer.__name__)
    parameters = factory.Sequence(
        lambda _: {
            name: type_(1234)
            for (name, type_) in TestConsumer.__annotations__.items()
        },
    )

    class Meta:
        model = models.ConsumerModel
