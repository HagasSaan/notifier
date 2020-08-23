import datetime
from typing import Dict

import freezegun
import pytest
from pytest_mock import MockFixture

from configuration.factories import (
    ConfigurationFactory,
    SkipKeywordFactory,
    UserFactory,
)
from helpers.messages_components import Message
from message_producers.factories import TestProducer


@pytest.mark.parametrize(
    'kwargs', [
        {'producer': None, 'consumer': None},
        {'producer': None},
        {'consumer': None},
    ],
)
def test_run_configuration_raises_error_if_consumer_or_producer_not_specified(
    db: MockFixture,
    kwargs: Dict[str, None],
) -> None:
    configuration = ConfigurationFactory(**kwargs)

    with pytest.raises(
        ValueError,
        match='Error: consumer or producer not specified',
    ):
        configuration.run()


@freezegun.freeze_time('15:00:00')
def test_run_configuration(
    db: MockFixture,
    mocker: MockFixture,
) -> None:
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
    user_not_working = UserFactory(
        on_leave=True,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )
    user_not_in_config = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )

    skip_keyword = SkipKeywordFactory()

    fake_messages = [
        Message(user1.username, user2.username, 'message1'),
        Message(user2.username, user1.username, 'message2'),
        Message(user2.username, user_not_working.username, 'message to not working user'),
        Message(user2.username, user1.username, f'message with {skip_keyword.word}'),
        Message(user2.username, user_not_in_config.username, 'messsage to not in config user'),
    ]

    mocker.patch.object(TestProducer, 'produce_messages', return_value=fake_messages)

    configuration = ConfigurationFactory(
        users=(user1, user2, user_not_working),
        skip_keywords=(skip_keyword,),
    )

    configuration.run()
