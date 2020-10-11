from typing import Union

from django.core.exceptions import ValidationError
from django.db import models

from helpers.registry import Registry
from helpers.traits import Validatable
from message_consumers.consumers.message_consumer import MessageConsumer
from message_producers.producers.message_producer import MessageProducer


DEFAULT_REGISTRY_NAME = 'default'


class ABCObjectModel(models.Model):
    REGISTRY_NAME = DEFAULT_REGISTRY_NAME
    CUSTOM_OBJECT_MODEL = None

    name = models.CharField(max_length=100, unique=True)
    object_type = models.CharField(max_length=100, choices=[])
    parameters = models.JSONField(blank=True, default=dict)

    class Meta:
        abstract = True

    @classmethod
    def notify(cls) -> None:
        """
        Notification comes when registry updated (new custom object added)
        """
        object_type = cls._meta.get_field('object_type')
        object_type.choices = [
            (key, key)
            for key in Registry(cls.REGISTRY_NAME).keys
        ]

    def __str__(self):
        return f'{self.object_type} "{self.name}"'

    def save(self, **kwargs: dict) -> None:
        self._check_params_before_save()
        super().save(**kwargs)

    def _check_params_before_save(self) -> None:
        class_ = Registry(self.REGISTRY_NAME).get(self.object_type)
        if issubclass(class_, Validatable):
            try:
                class_.validate_params(self.parameters)
            except Exception as e:
                # TODO: Specify exceptions
                # Now it masks exceptions of attributes of classes
                required_fields = '\t\n'.join(
                    [
                        f'{name}:{type_}'
                        for name, type_ in class_.__annotations__.items()
                    ],
                )
                raise ValidationError(
                    f'Error: {e}\n'
                    f'Required fields for {self.object_type} is: \n'
                    f'\t{required_fields}',
                )

    def get_object_by_registry_name(
        self,
        registry_name: str,
    ) -> Union[MessageConsumer, MessageProducer]:
        registry = Registry(registry_name)
        class_ = registry.get(self.object_type)
        object_ = class_(**self.parameters)
        return object_
