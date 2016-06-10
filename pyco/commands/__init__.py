# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-12'

This init will contain the classes that implement all commands.

Commands can be added to PyCo just importing them here, all
classes that extend 'BaseCommand' will be automatically
resolved by pyco.core.resolver.
Try to aggregate commands in proper modules so that it is
easier find them.

Example on how to write a command can be found in the
module pyco.commands.examples. Over there you can also find
more details.
"""

from base import *
from stats import *
from visualization import *
from iofile import *
