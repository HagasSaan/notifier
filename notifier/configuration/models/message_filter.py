from helpers.abc_object_model import ABCObjectModel
from helpers.messages_components.message_filters import MESSAGE_FILTER_REGISTRY_NAME


class MessageFilterModel(ABCObjectModel):
    REGISTRY_NAME = MESSAGE_FILTER_REGISTRY_NAME
