import datetime
from typing import Tuple, List

import freezegun
import pytest
from pytest_mock import MockFixture

from configuration.factories import UserFactory, SkipKeywordFactory, ConfigurationFactory
from configuration.models import User
from . import InternalMessage
from .message_filters import (
    SkipKeywordsMessageFilter,
    ReceiverExistsMessageFilter,
    ReceiverWorkingMessageFilter,
)

@pytest.fixture
def setup(db: MockFixture) -> Tuple[User, User, List[InternalMessage]]:
    user1, user2 = [
        UserFactory(
            on_leave=False,
            working_time_start=datetime.time(8, 0, 0),
            working_time_end=datetime.time(17, 0, 0),
        )
        for _ in range(2)
    ]

    messages_should_be_consumed = [
        InternalMessage(user1, user2, 'message1'),
        InternalMessage(user2, user1, 'message2'),
    ]

    return user1, user2, messages_should_be_consumed


@freezegun.freeze_time('15:00:00')
def test_skip_messages_filter(
    db: MockFixture,
    setup: Tuple[User, User, List[InternalMessage]],
) -> None:
    user1, user2, messages_should_be_consumed = setup

    skip_keyword = SkipKeywordFactory()

    configuration = ConfigurationFactory(
        users=(user1, user2,),
        skip_keywords=(skip_keyword,),
    )

    fake_messages = messages_should_be_consumed + [
        InternalMessage(user2.username, user1.username, f'message with {skip_keyword.word}'),
    ]

    assert messages_should_be_consumed == SkipKeywordsMessageFilter()(
        fake_messages,
        configuration,
    )


@freezegun.freeze_time('15:00:00')
def test_receiver_exists_filter(
    db: MockFixture,
    setup: Tuple[User, User, List[InternalMessage]],
) -> None:
    user1, user2, messages_should_be_consumed = setup
    user_not_in_config = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )

    fake_messages = messages_should_be_consumed + [
        InternalMessage(user2, user_not_in_config, 'message to not in config user'),
    ]

    configuration = ConfigurationFactory(
        users=(user1, user2,),
    )

    assert messages_should_be_consumed == ReceiverExistsMessageFilter()(
        fake_messages,
        configuration,
    )


@freezegun.freeze_time('15:00:00')
def test_receiver_working_filter(
    db: MockFixture,
    setup: Tuple[User, User, List[InternalMessage]],
) -> None:
    user1, user2, messages_should_be_consumed = setup
    user_not_working = UserFactory(
        on_leave=True,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )

    fake_messages = messages_should_be_consumed + [
        InternalMessage(user2, user_not_working, 'message to not working user'),
    ]

    configuration = ConfigurationFactory(
        users=(user1, user2, user_not_working,),
    )

    assert messages_should_be_consumed == ReceiverWorkingMessageFilter()(
        fake_messages,
        configuration,
    )
