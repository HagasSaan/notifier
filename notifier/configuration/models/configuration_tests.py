import pytest
from pytest_mock import MockFixture

from message_consumers.factories import ConsumerModelFactory
from message_producers.factories import ProducerModelFactory
from .configuration import Configuration


@pytest.fixture
def m_configuration_without_producer_and_consumer(
    db: MockFixture,
) -> Configuration:
    return Configuration.objects.create(
        name='Test Configuration',
    )


@pytest.fixture
def m_configuration(
    db: MockFixture,
) -> Configuration:
    return Configuration.objects.create(
        name='Test Configuration',
        consumer=ConsumerModelFactory(),
        producer=ProducerModelFactory(),
    )


def test_run_configuration_raises_error_if_consumer_or_producer_not_specified(
    m_configuration_without_producer_and_consumer: Configuration,
) -> None:
    with pytest.raises(
        ValueError,
        match='Error: consumer or producer not specified',
    ):
        m_configuration_without_producer_and_consumer.run()


def test_run_configuration(m_configuration: Configuration) -> None:
    m_configuration.run()
