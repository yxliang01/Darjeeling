# -*- coding: utf-8 -*-
"""
This module provides the base Transformation class, from which all
transformation schemas inherit.
"""
__all__ = ('Transformation', 'TransformationSchema')

from typing import Any, List, Type, Iterator, TypeVar, Generic, Mapping
from typing_extensions import final
import abc
import typing

from ..core import Replacement, FileLine
from ..exceptions import (NameInUseException,
                          UnknownTransformationSchemaException)
from ..snippet import SnippetDatabase

if typing.TYPE_CHECKING:
    from ..problem import Problem

T = TypeVar('T', bound='Transformation')


class Transformation(abc.ABC):
    """Represents a source code transformation."""
    @abc.abstractmethod
    def to_replacement(self) -> Replacement:
        """Converts a transformation into a source code replacement."""
        ...


class TransformationSchema(Generic[T], abc.ABC):
    @abc.abstractmethod
    def all_at_lines(self,
                     lines: List[FileLine]
                     ) -> Mapping[FileLine, Iterator['Transformation']]:
        """
        Returns a mapping from lines to streams of all the possible
        transformations of this type that can be performed at that line.
        """
        ...
