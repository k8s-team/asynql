from __future__ import annotations

import sys

from abc import ABCMeta
from copy import deepcopy
from typing import Dict, Union, Any, List

from pydantic.utils import resolve_annotations

from asynql.gqlfield import Field
from asynql.gqlquery import GQLQuery


def _add_fields_from_base_classes(
    bases: List[Any]
) -> Dict[str, Union[Field, GQLModel]]:

    fields: Dict[str, Union[Field, GQLModel]] = {}
    for base in reversed(bases):
        if issubclass(base, GQLModel) and base != GQLModel:
            fields.update(deepcopy(base.__fields__))
    return fields


def _get_annotations(namespace: Dict[str, Any]) -> Dict[str, Any]:
    anno_types = namespace.get('__annotations__', {})
    if sys.version_info >= (3, 7):
        anno_types = resolve_annotations(
            anno_types,
            namespace.get('__module__', None)
        )
    return anno_types


def _get_fields_from_annotations(
    anno_types: Dict[str, Any],
    namespace: Dict[str, Any],
    fields: Dict[str, Union[Field, GQLModel]]
) -> Dict[str, Union[Field, GQLModel]]:
    for ann_name, ann_type in anno_types.items():
        if ann_name.startswith('_') or ann_name in namespace:
            continue

        if issubclass(ann_type, GQLModel):
            fields[ann_name] = ann_type(ann_name)
        else:
            fields[ann_name] = Field(ann_name)
    return fields


class MetaModel(ABCMeta):

    def __new__(mcs, name, bases, namespace):
        fields = _add_fields_from_base_classes(bases)
        anno_types = _get_annotations(namespace)
        fields = _get_fields_from_annotations(
            anno_types=anno_types,
            namespace=namespace,
            fields=fields
        )

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
