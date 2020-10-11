import pytest
from django.contrib.admin import AdminSite
from django.test import override_settings
from pytest_mock import MockFixture

from .admin import ConfigurationAdmin
from .models import Configuration


@pytest.fixture
def f_configuration_admin() -> ConfigurationAdmin:
    return ConfigurationAdmin(Configuration, AdminSite())


@override_settings(SYNC_MODE=True)
def test_run_configurations_sync_mode(
    f_configuration_admin: ConfigurationAdmin,
    mocker: MockFixture,
) -> None:
    f_configurations = [mocker.MagicMock() for _ in range(2)]
    f_configuration_admin.run_configurations(
        mocker.MagicMock(),
        f_configurations,
    )
    for f_config in f_configurations:
        f_config.run.assert_called_once()
