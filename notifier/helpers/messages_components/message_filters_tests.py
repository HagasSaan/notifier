import datetime
from typing import Tuple, List

import pytest
from pytest_mock import MockFixture

from configuration.factories import UserFactory, SkipKeywordFactory
from configuration.models import User
from . import Message
from .message_filters import SkipKeywordsMessageFilter


@pytest.fixture
def setup(db: MockFixture) -> Tuple[User, User, List[Message]]:
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
        Message(user1.username, user2.username, 'message1'),
        Message(user2.username, user1.username, 'message2'),
    ]

    return user1, user2, messages_should_be_consumed


def test_skip_messages_filter(
    db: MockFixture,
    setup: Tuple[User, User, List[Message]],
) -> None:
    user1, user2, messages_should_be_consumed = setup

    skip_keyword = SkipKeywordFactory()

    fake_messages = messages_should_be_consumed + [
        Message(user2.username, user1.username, f'message with {skip_keyword.word}'),
    ]
    assert messages_should_be_consumed == SkipKeywordsMessageFilter()(
        fake_messages,
        skip_keywords=[skip_keyword.word],
    )
