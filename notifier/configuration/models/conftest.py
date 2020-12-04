import datetime

import pytest

from configuration.factories import UserFactory
from configuration.models import User
from helpers.messages_components import ExternalMessage


@pytest.fixture
@pytest.mark.usefixtures('db')
def setup() -> tuple[User, User, list[ExternalMessage]]:
    user1 = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )
    user2 = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )

    messages_should_be_consumed = [
        ExternalMessage(user1.username, user2.username, 'message1'),
        ExternalMessage(user2.username, user1.username, 'message2'),
    ]

    return user1, user2, messages_should_be_consumed
