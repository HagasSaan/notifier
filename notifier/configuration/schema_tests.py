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
                Producers {
                    id
                    name
                    parameters
                }
                Consumers {
                    id
                    name
                    parameters
                }
                users {
                    id
                }
                MessageFilters {
                    id
                }
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
    producers = [ProducerModelFactory() for _ in range(2)]
    consumers = [ConsumerModelFactory() for _ in range(2)]
    users = [UserFactory() for _ in range(2)]
    response = graphql_query(
        """
        mutation {
            configuration(
                input: {
                    name: "fuck_muasdltiplit"
                    Consumers: [""" + ','.join(str(consumer.id) for consumer in consumers) + """]
                    Producers: [""" + ','.join(str(producer.id) for producer in producers) + """]
                    users: [""" + ','.join(str(user.id) for user in users) + """]
                }
            ) {
            configuration {
                id
                name
                Producers {
                    id
                }
                Consumers {
                    id
                }
                users {
                    id
                }
                MessageFilters {
                    id
                }
            }
            }
        }
        """,
        client=client,
    )
    content = json.loads(response.content)

    assert 'errors' not in content
