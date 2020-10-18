from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from .forms import ConsumerModelForm
from .models import ConsumerModel


class ConsumerModelType(DjangoObjectType):
    class Meta:
        model = ConsumerModel


class ConsumerModelMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ConsumerModelForm
