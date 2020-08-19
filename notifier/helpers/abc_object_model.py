from typing import Union

from django.core.exceptions import ValidationError
from django.db import models

from helpers.messages_components import CanProduceMessages, CanConsumeMessages
from helpers.registry import Registry


class ABCObjectModel(models.Model):
    DEFAULT_REGISTRY = Registry('default')

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(
        max_length=100,
        choices=[
            (key, key)
            for key in DEFAULT_REGISTRY.keys
        ]
    )

    parameters = models.JSONField()

    def __str__(self):
        return f'{self.type} "{self.name}"({self.__class__.__name__})'

    class Meta:
        abstract = True

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        class_: Union[CanProduceMessages, CanConsumeMessages] = \
            self.DEFAULT_REGISTRY.get(self.type)
        try:
            class_.validate_params(self.parameters)
        except TypeError as e:
            required_fields = '\t\n'.join(
                [
                    f'{name}:{type_}'
                    for name, type_ in class_.__annotations__.items()
                ]
            )
            raise ValidationError(
                f'Error: {e}\n'
                f'Required fields for {self.type} is: \n'
                f'\t{required_fields}'
            )
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
