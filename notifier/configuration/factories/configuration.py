import factory

from configuration.models import User, Configuration, MessageFilterModel
from message_consumers.factories import ConsumerModelFactory
from message_producers.factories import ProducerModelFactory


class ConfigurationFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'test_configuration_{x}')
    consumer = factory.SubFactory(ConsumerModelFactory)
    producer = factory.SubFactory(ProducerModelFactory)

    @factory.post_generation
    def users(self, create: bool, extracted: list[User]) -> None:
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)

    @factory.post_generation
    def message_filters(self, create: bool, extracted: list[MessageFilterModel]) -> None:
        if not create:
            return

        if extracted:
            for message_filter in extracted:
                self._message_filters.add(message_filter)

    class Meta:
        model = Configuration
