# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-18'
"""

import re

# Regex for command names
REGEX_COMMAND_NAME = re.compile('[a-z]*')

# Regex for the variable name loaded from .config
REGEX_VARIABLE_NAME = re.compile('^[a-z][a-z_\.]*[a-z\.]$')
