import pytest
from django.core.exceptions import ValidationError

from .telegram import TelegramGroupChat

# TODO: mock all before pushing to github


def test_validate_params():
    TelegramGroupChat.validate_params(
        {}
    )


def test_validate_params_should_raise_error():
    with pytest.raises(
        ValidationError,
    ):
        TelegramGroupChat.validate_params(
            {}
        )
