import json

import pytz
from django_celery_beat.models import PeriodicTask
from pytest_mock import MockFixture

from configuration.factories import ConfigurationFactory
from configuration.use_cases import ScheduleConfigurationUseCase


def test_schedule_configuration_use_case_creates_periodic_task(
    db: MockFixture,
) -> None:
    configuration = ConfigurationFactory()
    cleaned_data = {
        'minute': '*',
        'hour': '*',
        'day_of_week': '*',
        'day_of_month': '*',
        'month_of_year': '*',
        'timezone': pytz.UTC,
        'configuration': configuration,
    }
    ScheduleConfigurationUseCase(**cleaned_data).execute()

    assert PeriodicTask.objects.filter(
        task='configuration.tasks.run_configuration',
        kwargs=json.dumps({'configuration_id': configuration.id}),
    ).count() == 1
