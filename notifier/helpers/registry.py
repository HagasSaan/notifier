import structlog

from typing import Any, List

logger = structlog.get_logger(__name__)


class ItemAlreadyExists(Exception):
    pass


class ItemNotExists(Exception):
    pass


class Registry:
    _instances = {}

    def __init__(self, name: str):
        if self._instances.get(name) is None:
            self._instances[name] = {}
        self.name = name

    def __str__(self):
        return f'Registry {self.name}'

    def set(self, value: Any):
        key = value.__name__
        if self._instances[self.name].get(key) is not None:
            raise ItemAlreadyExists

        self._instances[self.name][key] = value

    def get(self, key: Any):
        value = self._instances[self.name].get(key)
        if value is None:
            raise ItemNotExists(
                f'Avaliable keys: {",".join(self._instances[self.name].keys())}\n'
                f'Requested key: {key}'
            )

        return value

    @property
    def keys(self) -> List[str]:
        return self._instances[self.name].keys()

    @staticmethod
    def get_registers():
        return Registry._instances.keys()

    @staticmethod
    def register(name):
        def _register_wrapper(class_):
            registry = Registry(name)
            registry.set(class_)
            logger.info(
                f'Class {class_.__name__} successfully '
                f'registered in {name} scope'
            )
            return class_

        return _register_wrapper
