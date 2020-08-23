import datetime

from pytest_mock import MockFixture

from configuration.factories.user import UserFactory


def test_user_on_leave(db: MockFixture) -> None:
    user = UserFactory(
        working_time_start=datetime.time(0, 0, 0),
        working_time_end=datetime.time(23, 59, 59),
        on_leave=True,
    )
    assert not user.is_working_time
