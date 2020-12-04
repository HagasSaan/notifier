import asyncio

import structlog

from helpers.messages_components import InternalMessage
from message_consumers.consumers.message_consumer import MessageConsumer
from message_producers.producers.message_producer import MessageProducer
from notifier.celery import app

logger = structlog.get_logger(__name__)


@app.task
def run_configuration(configuration_id: int) -> None:
    from .models import Configuration
    logger.bind(configuration_id=configuration_id)
    try:
        configuration = Configuration.objects.get(id=configuration_id)
        configuration.run()
        logger.info('Configuration executed')
    except Exception as e:
        logger.exception(
            'Configuration execution failed',
            reason=str(e),
        )


@app.task(serializer='pickle')
def put_messages_to_consumer(consumer: MessageConsumer, messages: list[InternalMessage]) -> None:
    prepared_messages = consumer.translate_messages_from_internal_to_external(messages)
    asyncio.run(consumer.consume_messages(prepared_messages))


@app.task(serializer='pickle')
def get_messages_from_producer(producer: MessageProducer) -> list[InternalMessage]:
    raw_messages = asyncio.run(producer.produce_external_messages())
    return producer.translate_messages_from_external_to_internal(raw_messages)
