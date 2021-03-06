import dataclasses
from typing import Any


@dataclasses.dataclass
class ExternalMessage:
    """
    That type of message used by consumers and producers
    Sender and receiver as strings represent usernames in
    consumer/producer scope
    """
    sender: str
    receiver: str
    content: Any

    def __hash__(self):
        return (
            hash(self.sender)
            + hash(self.receiver)
            + hash(self.content)
        )


@dataclasses.dataclass
class InternalMessage:
    # TODO: get normal typing from config user
    sender: 'User'  # noqa F821
    receiver: 'User'  # noqa F821
    content: Any
