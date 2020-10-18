from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from .forms import ConfigurationForm, UserForm, MessageFilterModelForm
from .models import Configuration, User, MessageFilterModel


class ConfigurationType(DjangoObjectType):
    class Meta:
        model = Configuration


class ConfigurationMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ConfigurationForm


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserMutation(DjangoModelFormMutation):
    class Meta:
        form_class = UserForm


class MessageFilterModelType(DjangoObjectType):
    class Meta:
        model = MessageFilterModel


class MessageFilterModelMutation(DjangoModelFormMutation):
    class Meta:
        form_class = MessageFilterModelForm
