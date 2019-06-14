from __future__ import annotations

from io import StringIO
from typing import Any, Dict, Union

from asynql.gqlfield import Field


class GQLQuery:

    def __init__(self, name: str, **kwargs) -> None:
        self.__name1__ = name
        self._filters: Dict[str, Any] = kwargs
        self._builder: Dict[str, Any] = {}

    def add(self, field: Union[Field, GQLQuery], name: str) -> None:
        if isinstance(field, GQLQuery):
            self._builder[name] = field
        else:
            self._builder[name] = {}

    def to_gql(self, inner: bool = False) -> str:
        query_str = StringIO()
        query_str.write(self.__name1__)
        query_str = self._apply_filters(query_str)
        query_str = self._apply_builder(query_str)
        query = query_str.getvalue()
        return "{{ {query} }}".format(query=query) if not inner else query

    def _apply_filters(self, query: StringIO) -> StringIO:
        if not self._filters:
            return query

        query.write('(')
        for filter_key, filter_value in self._filters.items():
            query.write("{key}: {value}".format(key=filter_key,
                                                value=filter_value))
        query.write(")")
        return query

    def _apply_builder(self, query: StringIO) -> StringIO:
        query.write(" {")
        for kk, vv in self._builder.items():
            if isinstance(vv, GQLQuery):
                query.write(" ")
                query.write(vv.to_gql(True))
            else:
                query.write(" ")
                query.write(kk)
        query.write(" }")
        return query
