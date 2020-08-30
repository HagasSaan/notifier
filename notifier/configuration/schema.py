from graphene_django import DjangoObjectType

from .models import (
    Configuration,
    SkipKeyword,
    User,
)


class ConfigurationType(DjangoObjectType):
    class Meta:
        model = Configuration


class SkipKeywordType(DjangoObjectType):
    class Meta:
        model = SkipKeyword


class UserType(DjangoObjectType):
    class Meta:
        model = User
