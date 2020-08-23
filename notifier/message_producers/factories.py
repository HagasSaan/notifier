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

    @property
    def username_key(self) -> str:
        return 'test_producer'

    async def produce_messages(self) -> List[Message]:
        return [
            Message(
                sender='user1',
                receiver='user2',
                content='content from user1 to user2',
            ),
            Message(
                sender='user2',
                receiver='user1',
                content='content from user2 to user1',
            ),
        ]

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
