import abc
from typing import Any, List, Dict

from helpers.messages_components import CanConsumeMessages, Message


class Chat(CanConsumeMessages):
    @abc.abstractmethod
    async def send_message(
        self,
        message: Message,
        *args: List[Any],
        **kwargs: Dict[Any, Any],
    ) -> None:
        raise NotImplementedError
