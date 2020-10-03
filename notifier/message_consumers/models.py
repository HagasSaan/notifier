import structlog

from helpers.abc_object_model import ABCObjectModel
from helpers.registry import Registry
from .consumers.message_consumer import CONSUMER_REGISTRY_NAME

logger = structlog.get_logger(__name__)


class ConsumerModel(ABCObjectModel):
    REGISTRY_NAME = CONSUMER_REGISTRY_NAME


Registry(CONSUMER_REGISTRY_NAME).subscribe(ConsumerModel)
