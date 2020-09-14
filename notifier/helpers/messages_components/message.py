import dataclasses
from typing import Any


@dataclasses.dataclass
class ExternalMessage:
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
