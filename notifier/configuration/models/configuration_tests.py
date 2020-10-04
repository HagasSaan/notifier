import datetime
from typing import Dict, Tuple, List

import freezegun
import pytest
from pytest_mock import MockFixture

from configuration.factories import (
    ConfigurationFactory,
    UserFactory,
)
from configuration.factories.message_filter import MessageFilterModelFactory
from configuration.models import User
from helpers.messages_components import ExternalMessage
from helpers.messages_components.message_filters import (
    SkipKeywordsMessageFilter,
    ReceiverExistsMessageFilter,
    ReceiverWorkingMessageFilter,
)
from message_consumers.factories import SampleConsumer
from message_producers.factories import SampleProducer


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


@pytest.fixture
def setup(db: MockFixture) -> Tuple[User, User, List[ExternalMessage]]:
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


@freezegun.freeze_time('15:00:00')
def test_run_configuration_should_filter_message_where_receiver_doesnt_have_consumer_username(
    db: MockFixture,
    mocker: MockFixture,
    setup: Tuple[User, User, List[ExternalMessage]],
) -> None:
    user1, user2, messages_should_be_consumed = setup
    user_without_consumer_username = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )
    user_without_consumer_username.additional_info.pop(SampleConsumer.USERNAME_KEY)
    user_without_consumer_username.save()

    messages_should_be_consumed = [
        ExternalMessage(user1.username, user2.username, 'message1'),
        ExternalMessage(user2.username, user1.username, 'message2'),
    ]

    fake_messages = messages_should_be_consumed + [
        ExternalMessage(
            user1.username,
            user_without_consumer_username.username,
            'message to user without consumer username',
        ),
    ]

    mocker.patch.object(SampleProducer, 'produce_messages', return_value=fake_messages)

    consume_messages_spy = mocker.spy(SampleConsumer, 'consume_messages')

    configuration = ConfigurationFactory(
        users=(user1, user2, user_without_consumer_username),
    )

    configuration.run()

    assert consume_messages_spy.call_args.args[1] == messages_should_be_consumed


@freezegun.freeze_time('15:00:00')
def test_run_configuration_should_filter_message_where_receiver_is_not_working(
    db: MockFixture,
    mocker: MockFixture,
    setup: Tuple[User, User, List[ExternalMessage]],
) -> None:
    user1, user2, messages_should_be_consumed = setup
    user_not_working = UserFactory(
        on_leave=True,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )

    fake_messages = messages_should_be_consumed + [
        ExternalMessage(user2.username, user_not_working.username, 'message to not working user'),
    ]

    mocker.patch.object(SampleProducer, 'produce_messages', return_value=fake_messages)

    consume_messages_spy = mocker.spy(SampleConsumer, 'consume_messages')

    configuration = ConfigurationFactory(
        users=(user1, user2, user_not_working),
        message_filters=(
            MessageFilterModelFactory(object_type=ReceiverWorkingMessageFilter.__name__),
        ),
    )

    configuration.run()

    assert consume_messages_spy.call_args.args[1] == messages_should_be_consumed


@freezegun.freeze_time('15:00:00')
def test_run_configuration_should_filter_message_with_skip_keywords(
    db: MockFixture,
    mocker: MockFixture,
    setup: Tuple[User, User, List[ExternalMessage]],
) -> None:
    user1, user2, messages_should_be_consumed = setup

    fake_messages = messages_should_be_consumed + [
        ExternalMessage(user2.username, user1.username, 'message with skip_keyword1'),
    ]

    mocker.patch.object(SampleProducer, 'produce_messages', return_value=fake_messages)

    consume_messages_spy = mocker.spy(SampleConsumer, 'consume_messages')

    configuration = ConfigurationFactory(
        users=(user1, user2),
        message_filters=(
            MessageFilterModelFactory(
                object_type=SkipKeywordsMessageFilter.__name__,
                parameters={'skip_keywords': ['skip_keyword1']},
            ),
        ),
    )

    configuration.run()

    assert consume_messages_spy.call_args.args[1] == messages_should_be_consumed


@freezegun.freeze_time('15:00:00')
def test_run_configuration_should_filter_message_if_user_not_in_config(
    db: MockFixture,
    mocker: MockFixture,
    setup: Tuple[User, User, List[ExternalMessage]],
) -> None:
    user1, user2, messages_should_be_consumed = setup
    user_not_in_config = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )

    fake_messages = messages_should_be_consumed + [
        ExternalMessage(
            user2.username,
            user_not_in_config.username,
            'message to not in config user',
        ),
    ]

    mocker.patch.object(SampleProducer, 'produce_messages', return_value=fake_messages)

    consume_messages_spy = mocker.spy(SampleConsumer, 'consume_messages')

    configuration = ConfigurationFactory(
        users=(user1, user2),
        message_filters=(
            MessageFilterModelFactory(object_type=ReceiverExistsMessageFilter.__name__),
        ),
    )

    configuration.run()

    assert consume_messages_spy.call_args.args[1] == messages_should_be_consumed


@freezegun.freeze_time('15:00:00')
def test_run_configuration_should_filter_message_if_user_is_unknown(
    db: MockFixture,
    mocker: MockFixture,
    setup: Tuple[User, User, List[ExternalMessage]],
) -> None:
    user1, user2, messages_should_be_consumed = setup

    fake_messages = messages_should_be_consumed + [
        ExternalMessage('unknown_user', user1.username, 'message from unknown user'),
    ]

    mocker.patch.object(SampleProducer, 'produce_messages', return_value=fake_messages)
    consume_messages_spy = mocker.spy(SampleConsumer, 'consume_messages')

    configuration = ConfigurationFactory(
        users=(user1, user2),
    )
    configuration.run()

    assert consume_messages_spy.call_args.args[1] == messages_should_be_consumed
