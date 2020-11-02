import asyncio
from functools import reduce

import structlog
from django.db import models
from django.utils.functional import cached_property

from configuration.models import User, MessageFilterModel
from helpers.messages_components import ExternalMessage, InternalMessage
from helpers.messages_components.message_filters import (
    MESSAGE_FILTER_REGISTRY_NAME,
    BaseMessageFilter,
)
from message_consumers.consumers.message_consumer import MessageConsumer, CONSUMER_REGISTRY_NAME
from message_consumers.models import ConsumerModel
from message_producers.models import ProducerModel
from message_producers.producers.message_producer import MessageProducer, PRODUCER_REGISTRY_NAME

logger = structlog.get_logger(__name__)


class Configuration(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    _consumers = models.ManyToManyField(ConsumerModel, blank=True)
    _producers = models.ManyToManyField(ProducerModel, blank=True)
    _message_filters = models.ManyToManyField(MessageFilterModel, blank=True)

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'

    @cached_property
    def message_filters(self) -> list[type[BaseMessageFilter]]:
        return [
            message_filter.get_object_by_registry_name(MESSAGE_FILTER_REGISTRY_NAME)
            for message_filter in self._message_filters.all()
        ]

    @property
    def consumers(self) -> list[MessageConsumer]:
        return [
            consumer.get_object_by_registry_name(CONSUMER_REGISTRY_NAME)
            for consumer in self._consumers.all()
        ]

    @property
    def producers(self) -> list[MessageProducer]:
        return [
            producer.get_object_by_registry_name(PRODUCER_REGISTRY_NAME)
            for producer in self._producers.all()
        ]

    def run(self) -> None:
        # TODO: Maybe run as task?
        messages = []
        for producer in self.producers:
            raw_messages = asyncio.run(producer.produce_messages())
            messages += self._translate_message_users_from_producer_into_users(
                raw_messages,
                producer,
            )

        logger.info('Got messages', messages=messages)
        messages = reduce(
            lambda msgs, message_filter: message_filter(msgs, self),
            self.message_filters,
            messages,
        )

        # TODO: Maybe run as task?
        for consumer in self.consumers:
            asyncio.run(
                consumer.consume_messages(
                    self._translate_message_users_from_users_into_consumer(
                        messages,
                        consumer,
                    )
                )
            )

        logger.info('Messages consumed', messages=messages)

    @staticmethod
    def _translate_message_users_from_producer_into_users(
        messages: list[ExternalMessage],
        producer: MessageProducer,
    ) -> list[InternalMessage]:
        producer_username_key = producer.USERNAME_KEY

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
        messages: list[InternalMessage],
        consumer: MessageConsumer,
    ) -> list[ExternalMessage]:
        consumer_username_key = consumer.USERNAME_KEY

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
