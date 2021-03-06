# -*- coding: utf-8 -*-
import logging as _logging
import importlib as _importlib
import pkgutil as _pkgutil

from loguru import logger as _logger
_logger.disable('darjeeling')

from . import exceptions
from .version import __version__
from .environment import Environment
from .problem import Problem
from .events import (DarjeelingEvent, DarjeelingEventHandler,
                     DarjeelingEventProducer)


def _load_plugins() -> None:
    """Dynamically loads all plugins for Darjeeling."""
    for finder, name, is_pkg in _pkgutil.iter_modules():
        if name.startswith('darjeeling_'):
            _logger.info("loading plugin: %s", name)
            _importlib.import_module(name)


_load_plugins()
