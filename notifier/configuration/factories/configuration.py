import factory

from configuration import models


class ConfigurationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Configuration
