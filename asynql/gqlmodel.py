from __future__ import annotations

import sys

from abc import ABCMeta
from copy import deepcopy
from typing import Dict, Union, Any

from pydantic.utils import resolve_annotations

from asynql.gqlfield import Field
from asynql.gqlquery import GQLQuery


class MetaModel(ABCMeta):

    def __new__(mcs, name, bases, namespace):
        fields: Dict[str, Union[Field, GQLModel]] = {}
        for base in reversed(bases):
            if issubclass(base, GQLModel) and base != GQLModel:
                fields.update(deepcopy(base.__fields__))

        anno_types = namespace.get('__annotations__', {})
        if sys.version_info >= (3, 7):
            anno_types = resolve_annotations(
                anno_types,
                namespace.get('__module__', None)
            )

        for ann_name, ann_type in anno_types.items():
            if not ann_name.startswith('_') and ann_name not in namespace:
                if issubclass(ann_type, GQLModel):
                    fields[ann_name] = ann_type(ann_name)
                else:
                    fields[ann_name] = Field(ann_name)

        new_namespace = {
            '__fields__': fields,
            **{n: v for n, v in namespace.items() if n not in fields},
        }
        return super().__new__(mcs, name, bases, new_namespace)

    def __getattr__(self, item):
        return self.__fields__[item]


class GQLModel(metaclass=MetaModel):

    __one__ = ''
    __many__ = ''

    __slots__ = ('__name1__', '__values__', '__fields_set__')

    def __init__(self, name: str) -> None:
        self.__name1__ = name
        self.__values__: Dict[str, Any] = {}

    def q(self, *args: Union[Any, GQLQuery]) -> GQLQuery:
        query = GQLQuery(self.__name1__)
        for arg in args:
            query.add(arg, arg.__name1__)

        return query

    @classmethod
    def many(cls, *args: Union[Any, GQLQuery]) -> GQLQuery:
        query = GQLQuery(cls.__many__)
        for arg in args:
            query.add(arg, arg.__name1__)
        return query

    @classmethod
    def one(cls, *args: Union[Any, GQLQuery], **kwargs) -> GQLQuery:
        query = GQLQuery(cls.__one__, **kwargs)
        for arg in args:
            query.add(arg, arg.__name1__)
        return query
