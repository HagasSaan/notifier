import pytest

from .configuration import Configuration


@pytest.fixture
def m_configuration(db) -> Configuration:
    return Configuration.objects.create(
        name='Test configuration',
    )


def test_run_configuration_raises_error_if_consumer_or_producer_not_specified(
    m_configuration: Configuration,
) -> None:
    with pytest.raises(
        ValueError,
        match='Error: consumer or producer not specified',
    ):
        m_configuration.run()
