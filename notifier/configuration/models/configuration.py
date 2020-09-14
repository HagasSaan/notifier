import asyncio
from typing import List

import structlog
from django.db import models
from django.utils.functional import cached_property

from configuration.models import SkipKeyword, User, MessageFilterModel
from helpers.messages_components import ExternalMessage, InternalMessage
from helpers.messages_components.message_filters import (
    SkipKeywordsMessageFilter,
    ReceiverExistsMessageFilter,
    ReceiverWorkingMessageFilter,
)
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

        producer: MessageProducer = self.producer.get_object_by_registry_name(
            PRODUCER_REGISTRY_NAME,
        )
        consumer: MessageConsumer = self.consumer.get_object_by_registry_name(
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
        messages = ReceiverExistsMessageFilter()(
            messages,
            users=self.users.all(),
        )
        messages = ReceiverWorkingMessageFilter()(messages)
        messages = SkipKeywordsMessageFilter()(
            messages,
            skip_keywords=self.skip_keywords_list,
        )
        messages = self._translate_message_users_from_users_into_consumer(
            messages,
            consumer,
        )
        asyncio.run(consumer.consume_messages(messages))
        logger.info('Messages consumed', messages=messages)

    @staticmethod
    def _translate_message_users_from_producer_into_users(
        messages: List[ExternalMessage],
        producer: MessageProducer,
    ) -> List[InternalMessage]:
        producer_username_key = producer.username_key

        result_messages = []
        for message in messages:
            try:
                result_messages.append(
                    InternalMessage(
                        sender=User.get_user_by_producer_username(
                            message.sender,
                            producer_username_key,
                        ),
                        receiver=User.get_user_by_producer_username(
                            message.receiver,
                            producer_username_key,
                        ),
                        content=message.content,
                    ),
                )
            except User.DoesNotExist as e:
                logger.warning(f'Error: {e}')

        return result_messages

    @staticmethod
    def _translate_message_users_from_users_into_consumer(
        messages: List[InternalMessage],
        consumer: MessageConsumer,
    ) -> List[ExternalMessage]:
        consumer_username_key = consumer.username_key

        result_messages = []
        for message in messages:
            try:
                result_messages.append(
                    ExternalMessage(
                        sender=message.sender.get_consumer_username(
                            consumer_username_key,
                        ),
                        receiver=message.receiver.get_consumer_username(
                            consumer_username_key,
                        ),
                        content=message.content,
                    ),
                )
            except KeyError as e:
                logger.warning(f'Error: {e}')

        return result_messages
