import structlog

from helpers.abc_object_model import ABCObjectModel
from helpers.registry import Registry
from .consumers.message_consumer import CONSUMER_REGISTRY_NAME

logger = structlog.get_logger(__name__)


class ConsumerModel(ABCObjectModel):
    DEFAULT_REGISTRY = Registry(CONSUMER_REGISTRY_NAME)
