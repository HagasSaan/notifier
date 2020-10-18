import structlog

from typing import Any, Callable, KeysView

logger = structlog.get_logger(__name__)


class ItemAlreadyExists(Exception):
    pass


class ItemNotExists(Exception):
    pass


class Registry:
    _instances = {}
    _listeners = {}

    def __init__(self, name: str):
        if self._instances.get(name) is None:
            self._instances[name] = {}
            self._listeners[name] = []

        self.name = name

    def set(  # noqa A003
        self,
        value: Any,
        raise_if_exists: bool = True,
        notify_listeners: bool = True,
    ) -> None:
        key = value.__name__
        logger.info(
            f'Object {key} successfully '
            f'registered in {self.name} scope',
        )
        if self._instances[self.name].get(key) is not None and raise_if_exists:
            raise ItemAlreadyExists

        self._instances[self.name][key] = value

        if notify_listeners:
            self.notify_all()

    def notify_all(self) -> None:
        for listener in self._listeners[self.name]:
            listener.notify()

    def subscribe(self, listener: Any) -> None:
        self._listeners[self.name].append(listener)

    def get(self, key: Any) -> Any:
        value = self._instances[self.name].get(key)
        if value is None:
            raise ItemNotExists(
                f'Avaliable keys: {",".join(self._instances[self.name].keys())}\n'
                f'Requested key: {key}',
            )

        return value

    @property
    def keys(self) -> list[str]:
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
