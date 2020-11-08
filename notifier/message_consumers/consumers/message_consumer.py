import abc

import structlog

from helpers.messages_components import ExternalMessage, InternalMessage
from helpers.traits import Validatable

logger = structlog.get_logger(__name__)


class MessageConsumer(Validatable):
    USERNAME_KEY = 'default'

    @abc.abstractmethod
    async def consume_messages(self, messages: list[ExternalMessage]) -> None:
        raise NotImplementedError

    def translate_messages_from_internal_to_external(
        self,
        messages: list[InternalMessage],
    ) -> list[ExternalMessage]:
        consumer_username_key = self.USERNAME_KEY

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


CONSUMER_REGISTRY_NAME = 'Consumer'
