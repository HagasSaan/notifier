from unittest import mock

import pytest

from helpers.registry import (
    Registry,
    ItemNotExists,
    ItemAlreadyExists,
)


class RegisterTestClass:
    pass


@pytest.fixture
def f_registry() -> Registry:
    Registry.clean()
    return Registry('Test Registry')


def test_create_two_different_registers() -> None:
    Registry.clean()
    reg1 = Registry('reg1')
    reg1.set(RegisterTestClass)
    reg2 = Registry('reg2')
    reg2.set(RegisterTestClass)
    assert list(Registry.get_registers()) == ['reg1', 'reg2']


def test_creating_same_registers_returns_same_register() -> None:
    reg = Registry('Registry')
    assert len(reg.keys) == 0
    reg.set(RegisterTestClass)
    reg1 = Registry('Registry')
    assert RegisterTestClass.__name__ in reg1.keys


def test_add_class_to_registry(
    f_registry: Registry,
) -> None:
    f_registry.set(RegisterTestClass)
    assert f_registry.get(RegisterTestClass.__name__) == RegisterTestClass
    assert list(f_registry.keys) == [RegisterTestClass.__name__]


def test_add_class_to_registry_twice_raises_error(
    f_registry: Registry,
) -> None:
    f_registry.set(RegisterTestClass)
    with pytest.raises(ItemAlreadyExists):
        f_registry.set(RegisterTestClass)


def test_add_class_to_registry_twice_not_raises_error_with_special_flag(
    f_registry: Registry,
) -> None:
    f_registry.set(RegisterTestClass)
    f_registry.set(RegisterTestClass, raise_if_exists=False)


def test_add_class_notifies_listeners(
    f_registry: Registry,
) -> None:
    listeners = [mock.MagicMock() for _ in range(2)]
    [f_registry.subscribe(listener) for listener in listeners]
    f_registry.set(RegisterTestClass)
    assert all(listener.notify.called for listener in listeners)


def test_add_class_not_notifies_listeners_with_special_flag(
    f_registry: Registry,
) -> None:
    listener = mock.MagicMock()
    f_registry.subscribe(listener)
    f_registry.set(RegisterTestClass, notify_listeners=False)
    assert not listener.notify.called


def test_get_class_which_not_added_raises_error(
    f_registry: Registry,
) -> None:
    f_registry.set(RegisterTestClass)
    with pytest.raises(
        ItemNotExists,
        match=(
            f'Avaliable keys: {RegisterTestClass.__name__}\n'
            f'Requested key: unexpected_key'
        ),
    ):
        f_registry.get('unexpected_key')


def test_class_decorator() -> None:
    @Registry.register('Test')
    class RegisterTestClassDecorated:
        pass

    registry = Registry('Test')

    assert registry.get(RegisterTestClassDecorated.__name__) is RegisterTestClassDecorated
