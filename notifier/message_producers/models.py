import structlog

from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.abc_object_model import ABCObjectModel
from helpers.registry import Registry
from .producers.message_producer import PRODUCER_REGISTRY_NAME

logger = structlog.get_logger(__name__)


class CustomProducer(ABCCustomObjectModel):
    REGISTRY_NAME = PRODUCER_REGISTRY_NAME


class ProducerModel(ABCObjectModel):
    DEFAULT_REGISTRY = Registry(PRODUCER_REGISTRY_NAME)
    CUSTOM_OBJECT_MODEL = CustomProducer
