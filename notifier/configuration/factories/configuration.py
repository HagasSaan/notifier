from typing import List

import factory

from configuration.models import User, SkipKeyword, Configuration
from message_consumers.factories import ConsumerModelFactory
from message_producers.factories import ProducerModelFactory


class ConfigurationFactory(factory.django.DjangoModelFactory):
    name = 'test_configuration'
    consumer = factory.SubFactory(ConsumerModelFactory)
    producer = factory.SubFactory(ProducerModelFactory)

    @factory.post_generation
    def users(self, create: bool, extracted: List[User]) -> None:
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)

    @factory.post_generation
    def skip_keywords(self, create: bool, extracted: List[SkipKeyword]) -> None:
        if not create:
            return

        if extracted:
            for skip_keyword in extracted:
                self.skip_keywords.add(skip_keyword)

    class Meta:
        model = Configuration
