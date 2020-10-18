import dataclasses
import json

import pytz
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from .models import Configuration


@dataclasses.dataclass
class ScheduleConfigurationUseCase:
    minute: str
    hour: str
    day_of_week: str
    day_of_month: str
    month_of_year: str
    timezone: pytz.timezone
    configuration: Configuration

    def execute(self) -> None:
        kwargs = self.__dict__.copy()
        configuration = kwargs.pop('configuration')
        crontab, _ = CrontabSchedule.objects.get_or_create(**kwargs)
        PeriodicTask.objects.get_or_create(
            name=f'{str(configuration)}:{str(crontab)}',
            task='configuration.tasks.run_configuration',
            crontab=crontab,
            kwargs=json.dumps({'configuration_id': configuration.id}),
        )
