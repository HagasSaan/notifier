import datetime
import freezegun
from pytest_mock import MockFixture

from configuration.factories.user import UserFactory


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
