import graphene
from graphene_django import DjangoObjectType

from .models import (
    Configuration,
    User,
    MessageFilterModel,
)


class ConfigurationType(DjangoObjectType):
    class Meta:
        model = Configuration


class UserType(DjangoObjectType):
    class Meta:
        model = User


class MessageFilterType(DjangoObjectType):
    class Meta:
        model = MessageFilterModel


class ConfigurationsQuery(graphene.ObjectType):
    configurations = graphene.List(ConfigurationType)

    def resolve_configurations(root, info):
        return Configuration.objects.all()

