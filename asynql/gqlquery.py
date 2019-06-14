from __future__ import annotations

from typing import Any, Dict, Union


class GQLQuery:

    def __init__(self, name: str, query: Dict[str, Any] = None, **kwargs) -> None:
        self.__name1__ = name
        self._filters: Dict[str, Any] = kwargs
        self._query: Dict[str, Any] = query or {self.__name1__: {}}

    def add(self, field: Union[Field, GQLQuery], name: str) -> None:
        if isinstance(field, GQLQuery):
            self._query[self.__name1__][name] = field
        else:
            self._query[self.__name1__][name] = {}

    def to_gql(self, inner: bool = False) -> str:
        result = ""
        for k, v in self._query.items():
            if isinstance(v, dict):
                result += f"{k}"
                if self._filters:
                    filters = ""
                    for filter_key, filter_value in self._filters.items():
                        filters += f"{filter_key}: {filter_value}"
                    result += f"({filters})"

                result += " {"
                for kk, vv in v.items():
                    if isinstance(vv, GQLQuery):
                        result += f" {vv.to_gql(True)}"
                    else:
                        result += f" {kk}"
                result += " }"
        result = f"{{ {result} }}"  if not inner else result
        return result


from .gqlmodel import Field
