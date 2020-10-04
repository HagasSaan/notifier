import sys

from django.apps import AppConfig

from helpers.registry import Registry
from message_producers.producers.message_producer import PRODUCER_REGISTRY_NAME


class MessageProducersConfig(AppConfig):
    name = 'message_producers'

    def ready(self) -> None:
        if sys.argv[1] != 'runserver':
            return

        producer_model = self.get_model('ProducerModel')
        Registry(PRODUCER_REGISTRY_NAME).subscribe(producer_model)
        producer_model.CUSTOM_OBJECT_MODEL.get_all_custom_objects()
