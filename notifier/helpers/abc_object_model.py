from typing import Union, Any, Optional

from django.core.exceptions import ValidationError
from django.db import models

from helpers.registry import Registry
from helpers.traits import Validatable
from message_consumers.consumers.message_consumer import MessageConsumer
from message_producers.producers.message_producer import MessageProducer


DEFAULT_REGISTRY_NAME = 'default'


class ABCObjectModel(models.Model):
    DEFAULT_REGISTRY = Registry(DEFAULT_REGISTRY_NAME)

    name = models.CharField(max_length=100, unique=True)
    object_type = models.CharField(
        max_length=100,
        choices=[
            (key, key)
            for key in DEFAULT_REGISTRY.keys
        ],
    )

    parameters = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return f'{self.object_type} "{self.name}"({self.__class__.__name__})'

    class Meta:
        abstract = True

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[Any] = None,
        update_fields: Optional[Any] = None,
    ) -> None:
        self._check_params_before_save()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def _check_params_before_save(self) -> None:
        class_ = self.DEFAULT_REGISTRY.get(self.object_type)
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
