import abc
from typing import Any, List, Dict

from helpers.messages_components import MessageConsumer, Message


class Chat(MessageConsumer):
    @abc.abstractmethod
    async def send_message(
        self,
        message: Message,
        *args: List[Any],
        **kwargs: Dict[Any, Any],
    ) -> None:
        raise NotImplementedError
