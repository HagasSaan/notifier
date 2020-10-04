from typing import Dict, List, Any

from django.db import models

from helpers.registry import Registry

DEFAULT_REGISTRY_NAME = 'default'


class ABCCustomObjectModel(models.Model):
    REGISTRY_NAME = DEFAULT_REGISTRY_NAME

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=REGISTRY_NAME)

    class Meta:
        abstract = True

    @property
    def __name__(self):
        return str(self)

    def __str__(self):
        return f'{self.name}: {self.file}'

    def save(self, **kwargs: Dict) -> None:
        super().save(**kwargs)
        self._set_object(self)

    # TODO: delete object from registry when it deleted in DB

    def _set_object(self, object_: 'ABCCustomObjectModel') -> None:
        registry = Registry(self.REGISTRY_NAME)
        registry.set(object_)

    # TODO: incorrect name for that method
    @classmethod
    def get_all_custom_objects(cls) -> None:
        registry = Registry(cls.REGISTRY_NAME)
        for object_ in cls.objects.all():
            registry.set(
                object_,
                raise_if_exists=False,
                notify_listeners=False,
            )
        registry.notify_all()

    def __call__(
        self,
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> 'ABCCustomObjectModel':
        return self
