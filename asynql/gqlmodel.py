from __future__ import annotations

import sys

from abc import ABCMeta
from copy import deepcopy
from typing import Dict, Union, Any, ForwardRef, _eval_type, Optional


# from pydantic.utils import resolve_annotations
from mypy.types import AnyType


def resolve_annotations(raw_annotations: Dict[str, AnyType], module_name: Optional[str]) -> Dict[str, AnyType]:
    """
    Partially taken from typing.get_type_hints.

    Resolve string or ForwardRef annotations into type objects if possible.
    """
    if module_name:
        base_globals: Optional[Dict[str, Any]] = sys.modules[module_name].__dict__
    else:
        base_globals = None
    type_annotations = {}
    for name, value in raw_annotations.items():
        if isinstance(value, str):
            value = ForwardRef(value, is_argument=False)
        try:
            value = _eval_type(value, base_globals, None)
        except NameError:
            # this is ok, it can be fixed with update_forward_refs
            pass
        type_annotations[name] = value
    return type_annotations


class Field:

    def __init__(self, name: str) -> None:
        self.__name1__ = name


class MetaModel(ABCMeta):

    def __new__(mcs, name, bases, namespace):
        fields: Dict[str, Union[Field, GQLModel]] = {}
        for base in reversed(bases):
            if issubclass(base, GQLModel) and base != GQLModel:
                fields.update(deepcopy(base.__fields__))

        type_annotations = namespace.get('__annotations__', {})
        if sys.version_info >= (3, 7):
            type_annotations = resolve_annotations(type_annotations, namespace.get('__module__', None))

        if (namespace.get('__module__'), namespace.get('__qualname__')) != ('afisha_daily_sdk.gqlmodel', 'GQLModel'):
            for ann_name, ann_type in type_annotations.items():
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

    def __init__(self, name: str = None) -> None:
        values = {}
        object.__setattr__(self, '__values__', values)
        object.__setattr__(self, '__name1__', name)

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


from .gqlquery import GQLQuery
