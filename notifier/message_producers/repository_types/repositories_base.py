import abc
import dataclasses

import structlog

from helpers.initable import Initable
from helpers.messages_components import CanProduceMessages

logger = structlog.get_logger(__name__)


class PullRequest(Initable):
    pass


@dataclasses.dataclass
class Repository(CanProduceMessages):

    @abc.abstractmethod
    async def get_pull_requests(self):
        raise NotImplementedError
