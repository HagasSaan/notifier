from django.test import override_settings, Client
from django_celery_beat.models import PeriodicTask
from pytest_mock import MockFixture
from rest_framework.test import APIClient

from configuration.factories import UserFactory, ConfigurationFactory
from configuration.models import User
from configuration.serializers import ConfigurationSerializer


@override_settings(SYNC_MODE=True)
def test_run_configuration_in_api_sync_mode(db: MockFixture) -> None:
    configuration = ConfigurationFactory()
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        f'/restapi/configurations/'
        f'{configuration.id}/run_configuration/',
    )
    assert response.json() == {'status': 'success'}


@override_settings(SYNC_MODE=False)
def test_run_configuration_in_api_async_mode(
    db: MockFixture,
    mocker: MockFixture,
) -> None:
    configuration = ConfigurationFactory()
    mocker.patch('configuration.views.run_configuration_task')
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


def test_schedule_configuration_returns_form_on_get_request(
    db: MockFixture,
) -> None:
    User.objects.create_superuser(
        'superuser', 'superuser@test.com', 'superuser'
    )
    client = Client()
    client.login(username='superuser', password='superuser')
    response = client.get('/configuration/configuration/schedule_configuration/')
    assert response.status_code == 200


def test_schedule_configuration_returns_form_on_incorrect_post_request(
    db: MockFixture,
) -> None:
    configuration = ConfigurationFactory()
    User.objects.create_superuser(
        'superuser', 'superuser@test.com', 'superuser'
    )
    client = Client()
    client.login(username='superuser', password='superuser')
    response = client.post(
        '/configuration/configuration/schedule_configuration/',
        data={
            'minute': '142',
            'hour': '42',
            'day_of_week': '42',
            'day_of_month': '42',
            'month_of_year': '42',
            'timezone': 'UTC',
            'configuration': configuration.id,
        },
    )
    assert response.status_code == 200


def test_schedule_configuration_create_periodic_task_on_correct_post_request(
    db: MockFixture,
) -> None:
    configuration = ConfigurationFactory()
    User.objects.create_superuser(
        'superuser', 'superuser@test.com', 'superuser'
    )
    client = Client()
    client.login(username='superuser', password='superuser')
    response = client.post(
        '/configuration/configuration/schedule_configuration/',
        data={
            'minute': '*',
            'hour': '*',
            'day_of_week': '*',
            'day_of_month': '*',
            'month_of_year': '*',
            'timezone': 'UTC',
            'configuration': configuration.id,
        },
    )
    assert response.status_code == 302
    assert response.url == '/configuration/configuration/'

    assert PeriodicTask.objects.filter(
        kwargs='{"configuration_id": ' + str(configuration.id) + '}'
    ).count() == 1
