# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-13'
"""
from __future__ import print_function

import codecs
import platform
import sys

from colorama import init

from pyco.utils import disp
from pyco.version import __version__ as pyco_ver

disp('PyCo {0}'.format(pyco_ver))
disp('System: {0} {1}'.format(platform.system(), platform.release()))

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)
disp('stdout and stderr: utf8')

get_input = raw_input
if sys.version_info[0] >= 3:
    get_input = input

disp('input redirected: done')

disp('is tty: {0}'.format(sys.stdout.isatty()))

init(autoreset=True)
disp('colorama init: True')


