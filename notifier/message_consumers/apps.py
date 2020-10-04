import sys

from django.apps import AppConfig

from helpers.registry import Registry
from message_consumers.consumers.message_consumer import CONSUMER_REGISTRY_NAME


class MessageConsumersConfig(AppConfig):
    name = 'message_consumers'

    def ready(self) -> None:
        if sys.argv[1] != 'runserver':
            return

        consumer_model = self.get_model('ConsumerModel')
        Registry(CONSUMER_REGISTRY_NAME).subscribe(consumer_model)
        consumer_model.CUSTOM_OBJECT_MODEL.get_all_custom_objects()
