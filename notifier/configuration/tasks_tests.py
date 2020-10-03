from pytest_mock import MockFixture

from .factories import ConfigurationFactory
from .models import Configuration
from .tasks import run_configuration


def test_run_configuration(
    db: MockFixture,
    mocker: MockFixture,
    capsys: MockFixture,
) -> None:
    mocker.patch.object(Configuration, 'run')
    configuration = ConfigurationFactory()
    run_configuration(configuration.id)
    captured = capsys.readouterr()
    assert 'Configuration executed' in captured.out


def test_run_configuration_logs_error(
    db: MockFixture,
    mocker: MockFixture,
    capsys: MockFixture,
) -> None:
    mocker.patch.object(
        Configuration, 'run',
        side_effect=Exception('error occurred')
    )
    configuration = ConfigurationFactory()
    run_configuration(configuration.id)
    captured = capsys.readouterr()
    assert 'Configuration execution failed reason=error occurred' in captured.out
