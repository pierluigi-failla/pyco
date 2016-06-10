# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-16'

This will load all configs as
global variables (see pyco.core.global_variables)
so that if you need them you can access via
GlobalVariables singleton.

The config file '.config' sits in the same
folder of pyconsole.py
"""

import os.path

from pyco.core.exceptions import PyCoLoaderException
from pyco.core.global_variables import GlobalVariables
from pyco.core.parser import CommandParser
from pyco.core.regex import REGEX_VARIABLE_NAME
from pyco.core.resolver import CommandResolver
from pyco.utils import disp


class Loader(object):
    """This is special loader

    will process the provided file and
    will extract all the pairs key = value
    in it.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.isfile(self.file_path):
            raise PyCoLoaderException('Not valid file: "{0}"'.format(self.file_path))

    def load(self):
        """
        :return: a list of (key, values)
        """
        values = []
        with open(self.file_path, 'r') as fin:
            for line in fin:
                line = line.replace('\r', '').replace('\n', '').strip()
                if line.startswith('#'):  # skip comment lines
                    continue
                if not line:
                    continue
                parts = line.split('=')
                if len(parts) != 2:
                    raise PyCoLoaderException('Cannot decode file line: "{0}"'.format(line))
                key = parts[0].strip()
                if not REGEX_VARIABLE_NAME.match(key):
                    raise PyCoLoaderException('Not a valid name: "{0}"'.format(key))
                value = parts[1].strip()
                if key.endswith('_filename'):
                    # this is a file
                    value = os.path.abspath(value)
                values.append((key, value))
        return values


class AliasLoader(Loader):
    """This class loads the file '.alias'."""

    def __init__(self):
        super(AliasLoader, self).__init__(GlobalVariables.get_instance().get('aliases_filename'))
        command_resolver = CommandResolver.get_instance()
        for key, value in self.load():
            for cmd_name, options in CommandParser.parse(value):
                cmd_class, cmd_opts = command_resolver.get_class(cmd_name)
                if cmd_class is None:
                    raise PyCoLoaderException('Invalid alias: "{0} = {1}" (unknown "{2}")'.format(key,
                                                                                                  value,
                                                                                                  cmd_name))
                command_resolver.add(key, cmd_class, cmd_opts + options)


class ConfigLoader(Loader):
    """This class loads the file '.config'.

    Read the file and put values in GlobalVariables
    """

    def __init__(self, config_file_path):
        super(ConfigLoader, self).__init__(config_file_path)
        for key, value in self.load():
            disp('{0} = {1}'.format(key, value))
            GlobalVariables.get_instance().set(key, value)
