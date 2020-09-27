import re
from typing import Union, Dict

import pytest
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField
from pytest_mock import MockFixture

from . import Validatable
from .abc_object_model import ABCObjectModel, DEFAULT_REGISTRY_NAME
from .registry import Registry


@Registry.register(DEFAULT_REGISTRY_NAME)
class SampleClassInDefaultRegistry(Validatable):
    field_1: str
    field_2: int

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        if params['field_2'] != 42:
            raise ValidationError(
                'I need Answer to the Ultimate Question of Life, '
                'the Universe, and Everything as field_2 param'
            )


def test_validate_params(mocker: MockFixture) -> None:
    mocked_save = mocker.patch.object(models.Model, 'save')
    ABCObjectModel(
        name='just name',
        object_type=SampleClassInDefaultRegistry.__name__,
        parameters={
            'field_1': (
                'What is the Ultimate Question of Life, '
                'the Universe, and Everything'
            ),
            'field_2': 42
        },
    ).save()
    mocked_save.assert_called_once()


def test_validate_params_raise_error(db: MockFixture) -> None:
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '["Error: ['
            "'I need Answer to the Ultimate Question of Life, "
            'the Universe, and Everything as field_2 param'
            "']"
            '\\nRequired fields for SampleClassInDefaultRegistry is: '
            "\\n\\tfield_1:<class 'str'>"
            "\\t\\nfield_2:<class 'int'>"
            '"]'
        )
    ):
        ABCObjectModel(
            name='just name',
            object_type=SampleClassInDefaultRegistry.__name__,
            parameters={
                'field_1': (
                    'What is the Ultimate Question of Life, '
                    'the Universe, and Everything'
                ),
                'field_2': '1337'
            },
        ).save()


def test_validate_params_raise_error_if_fields_missing(db: MockFixture) -> None:
    with pytest.raises(
        ValidationError,
        match=re.escape(
            '["Error: '
            "'field_2'"
            '\\nRequired fields for SampleClassInDefaultRegistry is: '
            "\\n\\tfield_1:<class 'str'>"
            "\\t\\nfield_2:<class 'int'>"
            '"]'
        )
    ):
        ABCObjectModel(
            name='just name',
            object_type=SampleClassInDefaultRegistry.__name__,
            parameters={
                'field_1': (
                    'What is the Ultimate Question of Life, '
                    'the Universe, and Everything'
                ),
            },
        ).save()
