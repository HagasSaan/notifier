from django.test import override_settings
from pytest_mock import MockFixture
from rest_framework.test import APIClient

from configuration.factories import UserFactory, ConfigurationFactory
from configuration.serializers import ConfigurationSerializer


@override_settings(SYNC_MODE=True)
def test_run_configuration_in_api(db: MockFixture) -> None:
    configuration = ConfigurationFactory()
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        f'/restapi/configurations/'
        f'{configuration.id}/run_configuration/',
    )
    assert response.json() == {'status': 'success'}


def test_get_all_configurations_in_api(db: MockFixture) -> None:
    configurations = [ConfigurationFactory() for _ in range(2)]
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/restapi/configurations/')

    expected_configurations_json = [
        ConfigurationSerializer(configuration)
        for configuration in configurations
    ]
    for configuration in expected_configurations_json:
        configuration.context['request'] = response.wsgi_request

    expected_configurations_json = [
        configuration.data
        for configuration in expected_configurations_json
    ]

    actual_configurations_json = response.json()
    assert actual_configurations_json == expected_configurations_json
