import abc
from typing import get_origin, get_args, Any, Dict, List, Type


class InitError(Exception):
    pass


class Initable(abc.ABC):
    def __init__(self, kwargs: Dict[str, Any]):
        fields = self.__annotations__.items()
        for key, type_ in fields:
            origin_type = get_origin(type_)
            if origin_type is not None:
                if issubclass(origin_type, list):
                    self.__dict__[key] = self._handle_as_list(key, kwargs, type_)
            else:
                self.__dict__[key] = type_(kwargs[key])

    def _handle_as_list(
        self,
        key: str,
        kwargs: Dict[str, Any],
        type_: Type,
    ) -> List:
        result = []
        subtypes = get_args(type_)
        if len(subtypes) == 1:
            subtype = subtypes[0]
            for kwarg in kwargs[key]:
                result.append(subtype(kwarg))
        elif len(subtypes) == 0:
            for kwarg in kwargs[key]:
                result.append(kwarg)

        return result
