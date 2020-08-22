import asyncio
from datetime import datetime
from typing import List, Union

import structlog
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property

from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components import (
    CanConsumeMessages,
    CanProduceMessages,
    PRODUCER_REGISTRY_NAME,
    CONSUMER_REGISTRY_NAME,
    Message,
)
from helpers.registry import Registry
from message_consumers.models import ConsumerModel
from message_producers.models import ProducerModel


logger = structlog.get_logger(__name__)


# noinspection PyTypeChecker
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

    working_time_start = models.TimeField(
        default=datetime.now,
    )
    working_time_end = models.TimeField(
        default=datetime.now,
    )

    @property
    def is_working_time(self) -> bool:
        if self.on_leave:
            return False

        now = datetime.now().time()
        if not (self.working_time_start <= now <= self.working_time_end):
            return False

        return True


class SkipKeyword(models.Model):
    word = models.CharField(max_length=30)

    def __str__(self):
        return self.word


class Configuration(models.Model):
    name = models.CharField(max_length=100)
    skip_keywords = models.ManyToManyField(SkipKeyword)
    consumer: ConsumerModel = models.ForeignKey(
        ConsumerModel,
        null=True,
        on_delete=models.SET_NULL,
    )
    users = models.ManyToManyField(User)
    producer: ProducerModel = models.ForeignKey(
        ProducerModel,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'

    @cached_property
    def skip_keywords_list(self) -> List[str]:
        return [
            row['word']
            for row in self.skip_keywords.values('word')
        ]

    def run(self) -> None:
        producer: CanProduceMessages = self._get_object_by_model_and_registry(
            self.producer, PRODUCER_REGISTRY_NAME,
        )
        consumer: CanConsumeMessages = self._get_object_by_model_and_registry(
            self.consumer, CONSUMER_REGISTRY_NAME,
        )
        # TODO: Maybe run as task?
        messages = asyncio.run(producer.produce_messages())
        logger.info('Got messages', messages=messages)
        messages = self._translate_message_users_from_producer_into_users(
            messages,
            producer,
        )
        messages = self._filter_messages_where_receiver_not_in_config(messages)
        messages = self._filter_messages_where_receiver_is_not_working(messages)
        messages = self._filter_messages_with_skip_keywords(messages)
        messages = self._translate_message_users_from_users_into_consumer(
            messages,
            consumer,
        )
        asyncio.run(consumer.consume_messages(messages))
        logger.info('Messages consumed', messages=messages)

    def _filter_messages_with_skip_keywords(
        self,
        messages: List[Message],
    ) -> List[Message]:
        return [
            message
            for message in messages
            if not any(
                skip_keyword in message.content
                for skip_keyword in self.skip_keywords_list
            )
        ]

    def _filter_messages_where_receiver_not_in_config(
        self,
        messages: List[Message],
    ) -> List[Message]:
        return [
            message
            for message in messages
            if message.receiver in self.users.all()
        ]

    @staticmethod
    def _filter_messages_where_receiver_is_not_working(
        messages: List[Message],
    ) -> List[Message]:
        return [
            message
            for message in messages
            if message.receiver.is_working_time
        ]

    @staticmethod
    def _get_object_by_model_and_registry(
        object_model: ABCObjectModel,
        registry_name: str,
    ) -> Union[CanConsumeMessages, CanProduceMessages]:
        registry = Registry(registry_name)
        class_ = registry.get(object_model.type)
        object_ = class_(**object_model.parameters)
        return object_

    @staticmethod
    def _translate_message_users_from_producer_into_users(
        messages: List[Message],
        producer: CanProduceMessages,
    ) -> List[Message]:
        producer_username_key = producer.username_key

        result_messages = []
        for message in messages:
            try:
                message.sender = Configuration._get_user_by_producer_username(
                    message.sender,
                    producer_username_key,
                )
                message.receiver = Configuration._get_user_by_producer_username(
                    message.receiver,
                    producer_username_key,
                )
                result_messages.append(message)
            except User.DoesNotExist as e:
                logger.warning(f'Error: {e}')

        return result_messages

    @staticmethod
    def _translate_message_users_from_users_into_consumer(
        messages: List[Message],
        consumer: CanConsumeMessages,
    ) -> List[Message]:
        consumer_username_key = consumer.username_key

        result_messages = []
        for message in messages:
            try:
                message.sender = Configuration._get_consumer_username_by_user(
                    message.sender,
                    consumer_username_key,
                )
                message.receiver = Configuration._get_consumer_username_by_user(
                    message.receiver,
                    consumer_username_key,
                )
                result_messages.append(message)
            except KeyError as e:
                logger.warning(f'Error: {e}')

        return result_messages

    @staticmethod
    def _get_user_by_producer_username(
        username: str,
        producer_username_key: str,
    ) -> User:
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

    @staticmethod
    def _get_consumer_username_by_user(
        user: User,
        consumer_username_key: str,
    ) -> str:
        try:
            return user.additional_info[consumer_username_key]
        except KeyError:
            raise KeyError(
                f'User {user.username} does not contain data '
                f'about {consumer_username_key} scope',
            )
