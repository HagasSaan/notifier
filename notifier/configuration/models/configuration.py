import asyncio
from typing import List

import structlog
from django.db import models
from django.utils.functional import cached_property

from configuration.models import SkipKeyword, User, MessageFilterModel
from helpers.messages_components import Message
from message_consumers.consumers.message_consumer import MessageConsumer, CONSUMER_REGISTRY_NAME
from message_consumers.models import ConsumerModel
from message_producers.models import ProducerModel
from message_producers.producers.message_producer import MessageProducer, PRODUCER_REGISTRY_NAME

logger = structlog.get_logger(__name__)


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
    message_filters = models.ManyToManyField(MessageFilterModel)

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'

    @cached_property
    def skip_keywords_list(self) -> List[str]:
        return [
            row['word']
            for row in self.skip_keywords.values('word')
        ]

    def run(self) -> None:
        if self.consumer is None or self.producer is None:
            raise ValueError('Error: consumer or producer not specified')

        producer: MessageProducer = self.producer.get_object_by_registry(
            PRODUCER_REGISTRY_NAME,
        )
        consumer: MessageConsumer = self.consumer.get_object_by_registry(
            CONSUMER_REGISTRY_NAME,
        )
        # TODO: Maybe run as task?
        messages = asyncio.run(producer.produce_messages())
        logger.info('Got messages', messages=messages)
        messages = self._translate_message_users_from_producer_into_users(
            messages,
            producer,
        )
        # TODO: Move filters to their own class and make them pluggable
        messages = self._filter_messages_where_receiver_not_in_config(messages)
        messages = self._filter_messages_where_receiver_is_not_working(messages)
        messages = self._filter_messages_with_skip_keywords(
            messages,
            skip_keywords=self.skip_keywords,
        )
        messages = self._translate_message_users_from_users_into_consumer(
            messages,
            consumer,
        )
        asyncio.run(consumer.consume_messages(messages))
        logger.info('Messages consumed', messages=messages)

    @staticmethod
    def _filter_messages_with_skip_keywords(
        messages: List[Message],
        skip_keywords: List[str],
    ) -> List[Message]:
        return [
            message
            for message in messages
            if not any(
                skip_keyword in message.content
                for skip_keyword in skip_keywords
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
    def _translate_message_users_from_producer_into_users(
        messages: List[Message],
        producer: MessageProducer,
    ) -> List[Message]:
        producer_username_key = producer.username_key

        result_messages = []
        for message in messages:
            try:
                message.sender = User.get_user_by_producer_username(
                    message.sender,
                    producer_username_key,
                )
                message.receiver = User.get_user_by_producer_username(
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
        consumer: MessageConsumer,
    ) -> List[Message]:
        consumer_username_key = consumer.username_key

        result_messages = []
        for message in messages:
            try:
                message.sender = message.sender.get_consumer_username(
                    consumer_username_key,
                )
                message.receiver = message.receiver.get_consumer_username(
                    consumer_username_key,
                )
                result_messages.append(message)
            except KeyError as e:
                logger.warning(f'Error: {e}')

        return result_messages
