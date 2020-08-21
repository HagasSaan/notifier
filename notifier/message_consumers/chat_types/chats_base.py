import abc

from helpers.messages_components import CanConsumeMessages, Message


class Chat(CanConsumeMessages):
    @abc.abstractmethod
    async def send_message(self, message: Message, *args, **kwargs):
        raise NotImplementedError
