import factory

from configuration import models


class MessageFilterModelFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'message_filter_name_{x}')
    object_type = factory.LazyAttribute(lambda a: a.__name__)
    parameters = {}

    class Meta:
        model = models.MessageFilterModel
