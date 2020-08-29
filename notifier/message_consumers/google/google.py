import dataclasses
from typing import List, Any, Dict, Union

from django.db.models import JSONField

from helpers.messages_components import CONSUMER_REGISTRY_NAME, Message, MessageConsumer
from helpers.registry import Registry


@Registry.register(CONSUMER_REGISTRY_NAME)
@dataclasses.dataclass
class GoogleChat(MessageConsumer):

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        pass

    username_key = 'google_username'

    async def consume_messages(self, messages: List[Message]) -> None:
        pass

    async def send_message(
        self,
        message: Message,
        *args: List[Any],
        **kwargs: Dict[Any, Any],
    ) -> None:
        raise NotImplementedError
