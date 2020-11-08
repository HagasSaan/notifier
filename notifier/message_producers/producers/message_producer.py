import abc

import structlog

from helpers.messages_components import ExternalMessage, InternalMessage
from helpers.traits import Validatable

logger = structlog.get_logger(__name__)


class MessageProducer(Validatable):
    USERNAME_KEY = 'default'

    @abc.abstractmethod
    async def produce_messages(self) -> list[ExternalMessage]:
        raise NotImplementedError

    def translate_messages_from_external_to_internal(
        self,
        messages: list[ExternalMessage],
    ) -> list[InternalMessage]:
        from configuration.models import User

        producer_username_key = self.USERNAME_KEY

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


PRODUCER_REGISTRY_NAME = 'Producer'
