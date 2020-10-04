from unittest import mock

from django.db.models import Model
from pytest_mock import MockFixture

from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.registry import Registry


def test_upload_all_custom_objects_from_db_to_registry(
    db: MockFixture,
) -> None:
    # TODO: add some custom_objects to db
    ABCCustomObjectModel.upload_all_custom_objects_from_db_to_registry()
    # TODO: check all objects exists in registry
    # TODO: notify called once for all listeners


def test_save_object_add_it_to_registry(
    mocker: MockFixture,
) -> None:
    registry = Registry(ABCCustomObjectModel.REGISTRY_NAME)
    listeners = [mock.MagicMock() for _ in range(2)]
    [registry.subscribe(listener) for listener in listeners]
    f_save = mocker.patch.object(Model, 'save')

    custom_object = ABCCustomObjectModel()
    custom_object.save()

    f_save.assert_called_once()
    assert str(custom_object) in registry.keys
    assert all(listener.notify.called for listener in listeners)


def test_call_returns_object() -> None:
    custom_object = ABCCustomObjectModel()
    assert custom_object is custom_object()
