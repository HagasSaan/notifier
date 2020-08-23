import factory

from configuration import models


class SkipKeywordFactory(factory.django.DjangoModelFactory):
    word = 'skip_keyword_1'

    class Meta:
        model = models.SkipKeyword
