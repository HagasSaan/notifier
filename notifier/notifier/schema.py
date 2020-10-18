import graphene
from django.conf import settings
from graphene_django import DjangoListField
from graphene_django.debug import DjangoDebug

from configuration.schema import (
    ConfigurationMutation,
    ConfigurationType,
    UserType,
    UserMutation,
    MessageFilterModelType,
    MessageFilterModelMutation,
)
from message_consumers.schema import ConsumerModelMutation, ConsumerModelType
from message_producers.schema import ProducerModelMutation, ProducerModelType


class Query(graphene.ObjectType):
    configurations = DjangoListField(ConfigurationType)
    consumer_models = DjangoListField(ConsumerModelType)
    producer_models = DjangoListField(ProducerModelType)
    users = DjangoListField(UserType)
    message_filters = DjangoListField(MessageFilterModelType)

    if settings.DEBUG:
        debug = graphene.Field(DjangoDebug)


class Mutation(graphene.ObjectType):
    configuration = ConfigurationMutation.Field()
    consumer_model = ConsumerModelMutation.Field()
    producer_model = ProducerModelMutation.Field()
    users = UserMutation.Field()
    message_filters = MessageFilterModelMutation.Field()

    if settings.DEBUG:
        debug = graphene.Field(DjangoDebug)


schema = graphene.Schema(query=Query, mutation=Mutation)
