from django.db.models import Model
from pytest_mock import MockFixture

from helpers.abc_custom_object_model import ABCCustomObjectModel
from helpers.registry import Registry


def test_upload_all_custom_objects_from_db_to_registry(
    mocker: MockFixture,
) -> None:
    f_objects_manager = mocker.MagicMock()
    ABCCustomObjectModel.objects = f_objects_manager
    f_custom_objects = [
        ABCCustomObjectModel(name=f'custom_object_{i}')
        for i in range(2)
    ]
    f_objects_manager.all.return_value = f_custom_objects
    registry = Registry(ABCCustomObjectModel.REGISTRY_NAME)
    f_listeners = [mocker.MagicMock() for _ in range(2)]
    [registry.subscribe(listener) for listener in f_listeners]

    ABCCustomObjectModel.upload_all_custom_objects_from_db_to_registry()

    assert all(
        str(custom_object) in registry.keys
        for custom_object in f_custom_objects
    )
    [listener.notify.assert_called_once() for listener in f_listeners]


def test_save_object_add_it_to_registry(
    mocker: MockFixture,
) -> None:
    registry = Registry(ABCCustomObjectModel.REGISTRY_NAME)
    f_listeners = [mocker.MagicMock() for _ in range(2)]
    [registry.subscribe(listener) for listener in f_listeners]
    f_save = mocker.patch.object(Model, 'save')

    custom_object = ABCCustomObjectModel()
    custom_object.save()

    f_save.assert_called_once()
    assert str(custom_object) in registry.keys
    [listener.notify.assert_called_once() for listener in f_listeners]


def test_call_returns_object() -> None:
    custom_object = ABCCustomObjectModel()
    assert custom_object is custom_object()
