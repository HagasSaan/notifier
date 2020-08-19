import pytest

from helpers.registry import (
    Registry,
    ItemNotExists,
    ItemAlreadyExists,
)


class RegisterTestClass:
    def method(self):
        return self.__class__.__name__


@pytest.fixture
def f_registry() -> Registry:
    return Registry('Test Registry')


def test_create_two_different_registers():
    reg1 = Registry('reg1')
    reg1.set(RegisterTestClass)
    reg2 = Registry('reg2')
    reg2.set(RegisterTestClass)
    assert list(Registry.get_registers()) == ['reg1', 'reg2']


def test_creating_same_registers_returns_same_register():
    reg = Registry('Registry')
    assert len(reg.keys) == 0
    reg.set(RegisterTestClass)
    reg1 = Registry('Registry')
    assert RegisterTestClass.__name__ in reg1.keys


def test_add_class_to_registry(f_registry):
    f_registry.set(RegisterTestClass)
    assert f_registry.get(RegisterTestClass.__name__) == RegisterTestClass
    assert list(f_registry.keys) == [RegisterTestClass.__name__, ]


def test_add_class_to_registry_twice_raises_error(f_registry):
    f_registry.set(RegisterTestClass)
    with pytest.raises(ItemAlreadyExists):
        f_registry.set(RegisterTestClass)


def test_get_class_which_not_added_raises_error(f_registry):
    f_registry.set(RegisterTestClass)
    with pytest.raises(
        ItemNotExists,
        match=(
            f"Available keys: {RegisterTestClass.__name__}\n"
            f"Requested key: unexpected_key"
        )
    ):
        f_registry.get('unexpected_key')


def test_class_decorator():
    @Registry.register('Test')
    class RegisterTestClassDecorated:
        def method(self):
            return self.__class__.__name__

    registry = Registry('Test')

    assert registry.get(RegisterTestClassDecorated.__name__) is RegisterTestClassDecorated
