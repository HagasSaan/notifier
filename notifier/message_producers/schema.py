from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from .forms import ProducerModelForm
from .models import ProducerModel


class ProducerModelType(DjangoObjectType):
    class Meta:
        model = ProducerModel


class ProducerModelMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ProducerModelForm
