import abc
from typing import Union

from django.db.models import JSONField


class Validatable:
    @classmethod
    def validate_params(cls, params: Union[dict, JSONField]) -> None:
        pass
