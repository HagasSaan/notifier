import abc
from typing import Union

from django.db.models import JSONField


class Validatable:
    @classmethod
    @abc.abstractmethod
    def validate_params(cls, params: Union[dict, JSONField]) -> None:
        raise NotImplementedError
