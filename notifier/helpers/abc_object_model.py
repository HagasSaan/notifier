import abc
from typing import Union, Any, Optional, Dict

from django.core.exceptions import ValidationError
from django.db import models
from django.forms import JSONField

from helpers.registry import Registry
from message_consumers.consumers.message_consumer import MessageConsumer
from message_producers.producers.message_producer import MessageProducer


class ABCObjectModel(models.Model):
    DEFAULT_REGISTRY = Registry('default')

    name = models.CharField(max_length=100, unique=True)
    object_type = models.CharField(
        max_length=100,
        choices=[
            (key, key)
            for key in DEFAULT_REGISTRY.keys
        ],
    )

    parameters = models.JSONField()

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
        class_: 'ABCObjectModel' = (
            self.DEFAULT_REGISTRY.get(self.object_type)
        )
        try:
            class_.validate_params(self.parameters)
        except Exception as e:
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
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def get_object_by_registry(
        self,
        registry_name: str,
    ) -> Union[MessageConsumer, MessageProducer]:
        registry = Registry(registry_name)
        class_ = registry.get(self.object_type)
        object_ = class_(**self.parameters)
        return object_

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        raise NotImplementedError
