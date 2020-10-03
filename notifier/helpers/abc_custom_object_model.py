from typing import Dict

from django.db import models

from helpers.registry import Registry

DEFAULT_REGISTRY_NAME = 'default'


class ABCCustomObjectModel(models.Model):
    REGISTRY_NAME = DEFAULT_REGISTRY_NAME
    DEFAULT_REGISTRY = Registry(REGISTRY_NAME)
    UPLOAD_TO = REGISTRY_NAME

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=UPLOAD_TO)

    class Meta:
        abstract = True

    @property
    def __name__(self):
        return str(self)

    def __str__(self):
        return f'{self.name}: {self.file}'

    def save(self, **kwargs: Dict) -> None:
        super().save(**kwargs)
        self.get_all_custom_objects()

    @classmethod
    def get_all_custom_objects(cls) -> None:
        # TODO: может добавить фильтры того, что уже есть?
        #  а то не айс чёт
        #  еще вариант отображать конкретно добавленный объект
        custom_objects = cls.objects.all()
        for object_ in custom_objects:
            cls.DEFAULT_REGISTRY.set(object_, raise_if_exists=False)
