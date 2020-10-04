import datetime
import freezegun
import pytest
from pytest_mock import MockFixture

from configuration.factories.user import UserFactory
from configuration.models import User
from message_consumers.factories import SampleConsumer
from message_producers.factories import SampleProducer


@pytest.fixture
def default_user(db: MockFixture) -> User:
    user = UserFactory(
        working_time_start=datetime.time(0, 0, 0),
        working_time_end=datetime.time(23, 59, 59),
    )
    return user


def test_user_on_leave(db: MockFixture) -> None:
    user = UserFactory(
        working_time_start=datetime.time(0, 0, 0),
        working_time_end=datetime.time(23, 59, 59),
        on_leave=True,
    )
    assert not user.is_working_time


@freezegun.freeze_time('15:00:00')
def test_user_working(db: MockFixture) -> None:
    user = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )
    assert user.is_working_time


@freezegun.freeze_time('20:00:00')
def test_user_not_working(db: MockFixture) -> None:
    user = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )
    assert not user.is_working_time


@freezegun.freeze_time('02:00:00')
def test_user_working_night_shift(db: MockFixture) -> None:
    user = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(23, 0, 0),
        working_time_end=datetime.time(8, 0, 0),
    )
    assert user.is_working_time


@freezegun.freeze_time('20:00:00')
def test_user_not_working_night_shift(db: MockFixture) -> None:
    user = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(23, 0, 0),
        working_time_end=datetime.time(8, 0, 0),
    )
    assert not user.is_working_time


def test_get_user_by_producer_username(
    default_user: User,
) -> None:
    user = User.get_user_by_producer_username(
        default_user.username,
        SampleProducer.USERNAME_KEY,
    )
    assert user == default_user


def test_get_user_by_producer_username_raises_error_if_user_not_exists(
    default_user: User,
) -> None:
    with pytest.raises(
        User.DoesNotExist,
        match=(
            f'User with fake_producer_username_key:{default_user.username} '
            f'does not exist'
        ),
    ):
        User.get_user_by_producer_username(
            default_user.username,
            'fake_producer_username_key',
        )


def test_get_consumer_username(
    default_user: User,
) -> None:
    assert default_user.get_consumer_username(
        SampleConsumer.USERNAME_KEY,
    ) == default_user.username


def test_get_consumer_username_raises_error_if_user_without_consumer_username(
    default_user: User,
) -> None:
    with pytest.raises(
        KeyError,
        match=(
            f'User {default_user.username} does not contain data '
            f'about fake_consumer_username_key scope'
        ),
    ):
        default_user.get_consumer_username('fake_consumer_username_key')
