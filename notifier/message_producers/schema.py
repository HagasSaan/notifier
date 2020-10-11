from typing import Optional, Any

import graphene
from django.db.models import QuerySet
from graphene_django import DjangoObjectType

from helpers.registry import Registry
from message_producers.models import ProducerModel


class ProducerModelType(DjangoObjectType):
    class Meta:
        model = ProducerModel


class ProducerModelsQuery(graphene.ObjectType):
    producer_models = graphene.List(ProducerModelType)
    producer_types = graphene.List(
        graphene.String,
        producer_type=graphene.String(),
    )

    def resolve_producer_models(self, info: Any) -> QuerySet[ProducerModel]:
        return ProducerModel.objects.all()

    def resolve_producer_types(self, info: Any, producer_type: Optional[str] = None) -> list[str]:
        if producer_type is None:
            return Registry(ProducerModel.REGISTRY_NAME).keys

        producer_model = Registry(ProducerModel.REGISTRY_NAME).get(producer_type)
        return [f'producer_type: {producer_model.__name__}'] + [
            f'{name}: {field_info.type.__name__}'
            for name, field_info in producer_model.__dataclass_fields__.items()
        ]
