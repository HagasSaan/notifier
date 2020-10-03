import inspect
from typing import Union, Dict, Tuple, Any

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
    object_type = models.CharField(max_length=100, choices=[])
    parameters = models.JSONField(blank=True, default=dict)

    def __init__(
        self,
        *args: Tuple[Any, ...],
        **kwargs: Dict[str, Any],
    ):
        super().__init__(*args, **kwargs)
        object_type = self._meta.get_field('object_type')
        object_type.choices = [
            (key, key)
            for key in self.DEFAULT_REGISTRY.keys
        ]

    def __str__(self):
        return f'{self.object_type} "{self.name}"'

    class Meta:
        abstract = True

    def save(self, **kwargs: Dict) -> None:
        self._check_params_before_save()
        super().save(**kwargs)

    def _check_params_before_save(self) -> None:
        class_ = self.DEFAULT_REGISTRY.get(self.object_type)

        # TODO: make abstract class and remove that shit
        #  That created because CustomProducer is not a class
        if not inspect.isclass(class_):
            return

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
