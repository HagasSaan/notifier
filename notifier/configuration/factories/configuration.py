import factory

from configuration.models import User, Configuration, MessageFilterModel
from message_consumers.models import ConsumerModel
from message_producers.models import ProducerModel


class ConfigurationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Configuration

    name = factory.Sequence(lambda x: f'test_configuration_{x}')

    @factory.post_generation
    def users(self, _: bool, extracted: list[User]) -> None:
        if extracted:
            for user in extracted:
                self.users.add(user)

    @factory.post_generation
    def message_filters(self, _: bool, extracted: list[MessageFilterModel]) -> None:
        if extracted:
            for message_filter in extracted:
                self._message_filters.add(message_filter)

    @factory.post_generation
    def producers(self, _: bool, extracted: list[ProducerModel]) -> None:
        if extracted:
            for producer in extracted:
                self._producers.add(producer)

    @factory.post_generation
    def consumers(self, _: bool, extracted: list[ConsumerModel]) -> None:
        if extracted:
            for consumer in extracted:
                self._consumers.add(consumer)
