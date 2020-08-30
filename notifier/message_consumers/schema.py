from graphene_django import DjangoObjectType

from message_consumers.models import ConsumerModel


class ConsumerModelType(DjangoObjectType):
    class Meta:
        model = ConsumerModel
