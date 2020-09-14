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
        # TODO: do it in cycle, cuz new field can be added
        return (
            hash(self.sender)
            + hash(self.receiver)
            + hash(self.content)
        )


@dataclasses.dataclass
class InternalMessage:
    # TODO: get normal typing from config user
    sender: 'User'
    receiver: 'User'
    content: Any

    def __hash__(self):
        # TODO: do it in cycle, cuz new field can be added
        return (
            hash(self.sender)
            + hash(self.receiver)
            + hash(self.content)
        )
