import json

from django.test import Client
from graphene_django.utils.testing import graphql_query
from pytest_mock import MockFixture

from message_consumers.factories import ConsumerModelFactory
from message_producers.factories import ProducerModelFactory
from .factories import ConfigurationFactory, UserFactory


def test_get_all_configurations(
    client: Client,
    db: MockFixture,
) -> None:
    configurations = [ConfigurationFactory() for _ in range(2)]
    expected_configurations = {
        (configuration.id, configuration.name)
        for configuration in configurations
    }
    response = graphql_query(
        """
        query {
            configurations {
                id
                name
            }
        }
        """,
        client=client,
    )
    content = json.loads(response.content)

    assert 'errors' not in content

    actual_configurations = {
        (int(configuration['id']), configuration['name'])
        for configuration in content['data']['configurations']
    }

    assert actual_configurations == expected_configurations


def test_create_configuration(
    db: MockFixture,
    client: Client,
) -> None:
    producer = ProducerModelFactory()
    consumer = ConsumerModelFactory()
    user = UserFactory()
    response = graphql_query(
        """
        mutation {
            configuration(input: {
                name: "fuck"
                consumer: """ + str(consumer.id) + """
                producer: """ + str(producer.id) + """
                users: """ + str(user.id) + """
            }
            ) {
                configuration{
                    id   
                }
            }
        }
        """,
        client=client,
    )
    content = json.loads(response.content)

    assert 'errors' not in content
