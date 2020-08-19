import abc

from helpers.messages_components import CanConsumeMessages


class Chat(CanConsumeMessages):
    @abc.abstractmethod
    async def send_message(self, *args, **kwargs):
        raise NotImplementedError
