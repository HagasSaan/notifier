import dataclasses
from typing import List, Any, Dict, Union

from django.db.models import JSONField

from helpers.registry import Registry
from ..message_consumer import CONSUMER_REGISTRY_NAME, ExternalMessage, MessageConsumer


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class GoogleChat(MessageConsumer):

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        pass

    username_key = 'google_username'

    async def consume_messages(self, messages: List[ExternalMessage]) -> None:
        pass

    async def send_message(
        self,
        message: ExternalMessage,
        *args: List[Any],
        **kwargs: Dict[Any, Any],
    ) -> None:
        raise NotImplementedError
