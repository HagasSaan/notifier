from datetime import datetime

import factory

from configuration import models
from message_consumers.factories import SampleConsumer
from message_producers.factories import SampleProducer


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(
        lambda _: factory.Faker(
            'profile', fields=['username'],
        ).generate()['username'],
    )

    status = models.User.DEVELOPER_STATUS
    on_leave = False
    additional_info = factory.Dict(
        {
            SampleProducer.username_key: factory.SelfAttribute('..username'),
            SampleConsumer.username_key: factory.SelfAttribute('..username'),
        },
    )
    working_time_start = datetime.now().time()
    working_time_end = datetime.now().time()

    class Meta:
        model = models.User
