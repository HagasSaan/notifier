import structlog

from typing import Any, List, Callable, KeysView

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

    def set(self, value: Any, raise_if_exists: bool = True) -> None:  # noqa A003
        key = value.__name__
        logger.info(
            f'Object {key} successfully '
            f'registered in {self.name} scope',
        )
        if self._instances[self.name].get(key) is not None and raise_if_exists:
            raise ItemAlreadyExists

        self._instances[self.name][key] = value

    def get(self, key: Any) -> Any:
        value = self._instances[self.name].get(key)
        if value is None:
            raise ItemNotExists(
                f'Avaliable keys: {",".join(self._instances[self.name].keys())}\n'
                f'Requested key: {key}',
            )

        return value

    @property
    def keys(self) -> List[str]:
        return self._instances[self.name].keys()

    @staticmethod
    def get_registers() -> KeysView:
        return Registry._instances.keys()

    @staticmethod
    def register(name: str) -> Callable:
        def _register_wrapper(class_: object) -> object:
            registry = Registry(name)
            registry.set(class_)
            return class_

        return _register_wrapper

    @classmethod
    def clean(cls) -> None:
        cls._instances = {}
