from graphene_django import DjangoObjectType

from message_producers.models import ProducerModel


class ProducerModelType(DjangoObjectType):
    class Meta:
        model = ProducerModel
