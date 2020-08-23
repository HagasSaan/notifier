from datetime import datetime

import factory

from configuration import models
from message_consumers.factories import TestConsumer
from message_producers.factories import TestProducer


class UserFactory(factory.django.DjangoModelFactory):
    status = models.User.DEVELOPER_STATUS
    on_leave = False
    additional_info = {
        TestProducer.__name__: 'user1',
        TestConsumer.__name__: 'user2',
    }
    working_time_start = datetime.now().time()
    working_time_end = datetime.now().time()

    class Meta:
        model = models.User
