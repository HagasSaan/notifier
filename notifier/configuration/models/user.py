from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    DEVELOPER_STATUS = 'Developer'
    CODEOWNER_STATUS = 'Codeowner'
    STATUS_CHOICES = (
        (DEVELOPER_STATUS, DEVELOPER_STATUS),
        (CODEOWNER_STATUS, CODEOWNER_STATUS),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    on_leave = models.BooleanField(default=False)
    additional_info = models.JSONField(default=None, null=True, blank=True)
    working_time_start = models.TimeField(default=datetime.now)
    working_time_end = models.TimeField(default=datetime.now)

    @property
    def is_working_time(self) -> bool:
        if self.on_leave:
            return False

        now = datetime.now().time()
        if self.working_time_start <= now <= self.working_time_end:
            return True

        if (
            self.working_time_start > self.working_time_end
            and not (self.working_time_end <= now <= self.working_time_start)
        ):
            return True

        return False

    @staticmethod
    def get_user_by_producer_username(
        username: str,
        producer_username_key: str,
    ) -> 'User':
        try:
            return User.objects.get(
                additional_info__contains={
                    producer_username_key: username,
                },
            )
        except User.DoesNotExist:
            raise User.DoesNotExist(
                f'User with {producer_username_key}:{username} '
                f'does not exist',
            )

    def get_consumer_username(self, consumer_username_key: str) -> str:
        try:
            return self.additional_info[consumer_username_key]
        except KeyError:
            raise KeyError(
                f'User {self.username} does not contain data '
                f'about {consumer_username_key} scope',
            )
