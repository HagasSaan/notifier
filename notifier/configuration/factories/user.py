from datetime import datetime

import factory

from configuration import models
from message_consumers.factories import SampleConsumer
from message_producers.factories import SampleProducer


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.LazyAttribute(
        lambda _: factory.Faker(
            'profile', fields=['username'],
        ).generate()['username'],
    )

    on_leave = False
    additional_info = factory.Dict(
        {
            SampleProducer.USERNAME_KEY: factory.SelfAttribute('..username'),
            SampleConsumer.USERNAME_KEY: factory.SelfAttribute('..username'),
        },
    )
    working_time_start = datetime.now().time()
    working_time_end = datetime.now().time()
