from functools import reduce

import structlog
from django.db import models
from django.utils.functional import cached_property

from configuration import tasks
from configuration.models import User, MessageFilterModel
from helpers.messages_components import InternalMessage
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
        global logger
        logger = logger.bind(configuration_id=self.id)

        if len(self.producers) == 0 or len(self.consumers) == 0:
            logger.info('No producers or consumers, skipping...')
            return

        messages = self._produce_all_messages()

        logger.info('Got messages', messages=messages)
        messages = reduce(
            lambda msgs, message_filter: message_filter(msgs, self),
            self.message_filters,
            messages,
        )

        self._consume_all_messages(messages)

        logger.info('Messages consumed', messages=messages)

    def _consume_all_messages(self, messages) -> None:
        task_handlers = []
        for consumer in self.consumers:
            task_handlers.append(tasks.put_messages_to_consumer.delay(consumer, messages))

        [th.get() for th in task_handlers]

    def _produce_all_messages(self) -> list[InternalMessage]:
        task_handlers = []
        for producer in self.producers:
            task_handlers.append(
                tasks.get_messages_from_producer.delay(producer)
            )

        messages = []
        for th in task_handlers:
            messages.append(th.get())

        return messages
