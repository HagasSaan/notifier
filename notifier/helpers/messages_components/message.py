import dataclasses
from typing import Union, Any


@dataclasses.dataclass
class Message:
    # TODO: get normal typing from config user
    sender: Union[str, 'User']  # noqa F821
    receiver: Union[str, 'User']  # noqa F821
    content: Any

    def __hash__(self):
        # TODO: do it in cycle, cuz new field can be added
        return (
            hash(self.sender)
            + hash(self.receiver)
            + hash(self.content)
        )
