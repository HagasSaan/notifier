from typing import Optional, Any

import graphene
from django.db.models import QuerySet
from graphene_django import DjangoObjectType, DjangoListField

from helpers.registry import Registry
from message_consumers.models import ConsumerModel


class ConsumerModelType(DjangoObjectType):
    class Meta:
        model = ConsumerModel


class ConsumerModelsQuery(graphene.ObjectType):
    consumer_models = DjangoListField(ConsumerModelType)
    consumer_types = graphene.List(
        graphene.String,
        consumer_type=graphene.String(),
    )

    def resolve_consumer_models(self, info: Any) -> QuerySet[ConsumerModel]:
        return ConsumerModel.objects.all()

    def resolve_consumer_types(self, info: Any, consumer_type: Optional[str] = None) -> list[str]:
        if consumer_type is None:
            return Registry(ConsumerModel.REGISTRY_NAME).keys

        consumer_model = Registry(ConsumerModel.REGISTRY_NAME).get(consumer_type)
        return [f'consumer_type: {consumer_model.__name__}'] + [
            f'{name}: {field_info.type.__name__}'
            for name, field_info in consumer_model.__dataclass_fields__.items()
        ]
