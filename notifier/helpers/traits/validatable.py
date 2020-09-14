import abc
from typing import Union, Dict

from django.db.models import JSONField


class Validatable(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        raise NotImplementedError
