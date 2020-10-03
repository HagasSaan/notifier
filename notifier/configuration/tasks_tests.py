import pytest
from pytest_mock import MockFixture

from .factories import ConfigurationFactory
from .tasks import run_configuration


@pytest.mark.skip('Not working yet')
def test_run_configuration(db: MockFixture) -> None:
    configuration = ConfigurationFactory()
    run_configuration(configuration.id)


@pytest.mark.skip('Not working yet')
def test_run_configuration_logs_error() -> None:
    run_configuration(42)
