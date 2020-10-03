from typing import List, Any

import pytest

from helpers.traits import Initable


class InitableClassForTests(Initable):
    field_1: str
    field_2: int


def test_init_class_with_extra_args() -> None:
    args = {
        'field_1': 'string',
        'field_2': 4,
        'field_not_exists': {},
    }

    class_ = InitableClassForTests(args)

    assert class_.__dict__ == {
        'field_1': 'string',
        'field_2': 4,
    }


def test_init_class_without_required_args() -> None:
    args = {
        'field_1': 'string',
    }

    with pytest.raises(KeyError, match='field_2'):
        InitableClassForTests(args)


class ComplexInitableClassForTests(Initable):
    field_3: list
    complex_field: InitableClassForTests


def test_init_complex_class() -> None:
    args = {
        'field_3': ['string', 4],
        'complex_field': {
            'field_1': 'string',
            'field_2': 4,
            'field_not_exists': {},
        },
        'field_not_exists': 123,
    }

    class_ = ComplexInitableClassForTests(args)
    complex_field = class_.complex_field

    assert complex_field.__dict__ == {
        'field_1': 'string',
        'field_2': 4,
    }
    assert class_.__dict__ == {
        'field_3': ['string', 4],
        'complex_field': complex_field,
    }


def test_init_complex_class_without_required_args() -> None:
    args = {
        'field_3': ['string', 4],
        'complex_field': {
            'field_1': 'string',
            'field_not_exists': {},
        },
        'field_not_exists': 123,
    }

    with pytest.raises(KeyError, match='field_2'):
        ComplexInitableClassForTests(args)


class InitableClassWithTypingsForTests(Initable):
    field_1: List[str]
    field_2: List[InitableClassForTests]
    field_2_1: List
    # field_3: Dict[Any, Any]   # Not yet  # noqa: E800
    # field_4: Optional[Any]    # Not yet  # noqa: E800
    # field_4: Set[Any]         # Not yet  # noqa: E800


def test_init_class_with_typings() -> None:
    args = {
        'field_1': ['str_1', 'str_2'],
        'field_2': [
            {
                'field_1': 'ololo',
                'field_2': 123,
            },
            {
                'field_1': 'alala',
                'field_2': 456,
            },
        ],
        'field_2_1': [1, '2', True, 3.4],
    }
    class_ = InitableClassWithTypingsForTests(args)
    initable_classes = class_.field_2
    assert class_.__dict__ == {
        'field_1': ['str_1', 'str_2'],
        'field_2': initable_classes,
        'field_2_1': [1, '2', True, 3.4],
    }

