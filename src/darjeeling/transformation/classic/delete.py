# -*- coding: utf-8 -*-
__all__ = ('DeleteStatement',)

from typing import (List, Iterator, Iterable, Dict, Any, FrozenSet, Mapping,
                    Optional, ClassVar)
import typing

import attr
import kaskara

from .base import StatementTransformation, StatementTransformationSchema
from ..base import Transformation, TransformationSchema
from ..config import TransformationSchemaConfig
from ...snippet import SnippetDatabase, StatementSnippetDatabase
from ...core import (Replacement, FileLine, FileLocationRange, FileLocation,
                     FileLineSet, Location, LocationRange)
from ...exceptions import BadConfigurationException

if typing.TYPE_CHECKING:
    from ..problem import Problem


@attr.s(frozen=True, repr=False, auto_attribs=True)
class DeleteStatement(StatementTransformation):
    location: FileLocationRange

    def __repr__(self) -> str:
        s = "DeleteStatement<{}>".format(str(self.location))
        return s

    def to_replacement(self, problem: 'Problem') -> Replacement:
        return Replacement(self.location, '')

    @property
    def line(self) -> FileLine:
        return FileLine(self.location.filename,
                        self.location.start.line)

    class Schema(StatementTransformationSchema):
        def all_at_statement(self,
                             statement: kaskara.Statement
                             ) -> Iterator[Transformation]:
            problem = self._problem
            if problem.settings.ignore_decls and statement.kind == 'DeclStmt':
                return
            yield DeleteStatement(statement.location)

    class SchemaConfig(TransformationSchemaConfig):
        NAME: ClassVar[str] = 'delete-statement'

        @classmethod
        def from_dict(cls,
                      d: Mapping[str, Any],
                      dir_: Optional[str] = None
                      ) -> 'TransformationSchemaConfig':
            return DeleteStatement.SchemaConfig()

        def build(self,
                  problem: 'Problem',
                  snippets: SnippetDatabase
                  ) -> 'TransformationSchema':
            assert isinstance(snippets, StatementSnippetDatabase)
            return DeleteStatement.Schema(problem=problem, snippets=snippets)