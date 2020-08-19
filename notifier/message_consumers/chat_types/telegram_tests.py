import pytest
from django.core.exceptions import ValidationError

from .telegram import TelegramGroupChat


@pytest.mark.skip(reason='Not realized')
def test_validate_params():
    TelegramGroupChat.validate_params(
        {}
    )


@pytest.mark.skip(reason='Not realized')
def test_validate_params_should_raise_error():
    with pytest.raises(
        ValidationError,
    ):
        TelegramGroupChat.validate_params(
            {}
        )
