from typing import List

import graphene
from graphene_django import DjangoObjectType

from message_producers.models import ProducerModel


class ProducerModelType(DjangoObjectType):
    class Meta:
        model = ProducerModel
        exclude = ('parameters', )


class ProducerModelsQuery(graphene.ObjectType):
    producer_models = graphene.List(ProducerModelType)
    producer_types = graphene.List(
        graphene.String,
        producer_type=graphene.String()
    )

    def resolve_producer_models(root, info):
        return ProducerModel.objects.all()

    def resolve_producer_types(root, info, producer_type=None) -> List[str]:
        if producer_type is None:
            return ProducerModel.DEFAULT_REGISTRY.keys

        producer_model = ProducerModel.DEFAULT_REGISTRY.get(producer_type)
        return [f'producer_type: {producer_model.__name__}'] + [
            f'{name}: {field_info.type.__name__}'
            for name, field_info in producer_model.__dataclass_fields__.items()
        ]
