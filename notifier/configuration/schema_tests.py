import json

from django.test import Client
from graphene_django.utils.testing import graphql_query
from pytest_mock import MockFixture

from .factories import ConfigurationFactory


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
