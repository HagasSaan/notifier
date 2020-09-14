import factory

from configuration import models


class SkipKeywordFactory(factory.django.DjangoModelFactory):
    word = factory.Sequence(lambda x: f'skip_keyword_{x}')

    class Meta:
        model = models.SkipKeyword
