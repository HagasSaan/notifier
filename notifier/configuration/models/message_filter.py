from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components.message_filters import MESSAGE_FILTER_REGISTRY_NAME
from helpers.registry import Registry


class MessageFilterModel(ABCObjectModel):
    DEFAULT_REGISTRY = Registry(MESSAGE_FILTER_REGISTRY_NAME)
