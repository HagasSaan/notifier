from typing import List

import graphene
from graphene_django import DjangoObjectType, DjangoListField

from message_consumers.models import ConsumerModel


class ConsumerModelType(DjangoObjectType):
    class Meta:
        model = ConsumerModel
        exclude = ('parameters', )


class ConsumerModelsQuery(graphene.ObjectType):
    consumer_models = DjangoListField(ConsumerModelType)
    consumer_types = graphene.List(
        graphene.String,
        consumer_type=graphene.String()
    )

    def resolve_consumer_models(root, info):
        return ConsumerModel.objects.all()

    def resolve_consumer_types(root, info, consumer_type=None) -> List[str]:
        if consumer_type is None:
            return ConsumerModel.DEFAULT_REGISTRY.keys

        consumer_model = ConsumerModel.DEFAULT_REGISTRY.get(consumer_type)
        return [f'consumer_type: {consumer_model.__name__}'] + [
            f'{name}: {field_info.type.__name__}'
            for name, field_info in consumer_model.__dataclass_fields__.items()
        ]
