import datetime

import freezegun
import pytest
from django.contrib.admin import AdminSite
from django.test import override_settings
from pytest_mock import MockFixture

from .admin import ConfigurationAdmin, UserAdmin
from .factories import UserFactory
from .models import Configuration, User


@override_settings(SYNC_MODE=True)
def test_run_configurations_sync_mode(
    mocker: MockFixture,
) -> None:
    f_configurations = [mocker.MagicMock() for _ in range(2)]
    f_configuration_admin = ConfigurationAdmin(Configuration, AdminSite())
    f_configuration_admin.run_configurations(
        mocker.MagicMock(),
        f_configurations,
    )
    for f_config in f_configurations:
        f_config.run.assert_called_once()


@override_settings(SYNC_MODE=False)
def test_run_configurations_async_mode(
    mocker: MockFixture,
) -> None:
    f_configurations = [mocker.MagicMock() for _ in range(2)]
    f_configuration_admin = ConfigurationAdmin(Configuration, AdminSite())

    f_run_configuration = mocker.patch('configuration.admin.run_configuration')

    f_configuration_admin.run_configurations(
        mocker.MagicMock(),
        f_configurations,
    )
    f_run_configuration.delay.assert_has_calls(
        [mocker.call(conf.id) for conf in f_configurations],
    )


@pytest.mark.parametrize(
    'working_time, expected_is_working',
    [
        ('15:00:00', True),
        ('22:00:00', False),
    ],
)
def test_is_user_working_time(
    db: MockFixture,
    working_time: str,
    expected_is_working: bool,
) -> None:
    f_user_admin = UserAdmin(User, AdminSite())
    f_user = UserFactory(
        on_leave=False,
        working_time_start=datetime.time(8, 0, 0),
        working_time_end=datetime.time(17, 0, 0),
    )
    with freezegun.freeze_time(working_time):
        assert f_user_admin.is_working_time(f_user) == expected_is_working


def test_get_urls_contains_schedule_config_url() -> None:
    f_configuration_admin = ConfigurationAdmin(Configuration, AdminSite())
    urls = f_configuration_admin.get_urls()
    assert any(
        'schedule_configuration' in url.name
        for url in urls
    )
