# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-12'

This is the interface for the commands.

Basically you need to implement a class
derived from this one and implement the required
functions and the '__' attributes.

Command name can be just lower case see
pyco.core.regex to more details about
correct format.
"""

from abc import ABCMeta
from abc import abstractmethod

from pyco.core.decorators import TimeIt
from pyco.core.exceptions import PyCoCommandMalformedException
from pyco.core.regex import REGEX_COMMAND_NAME
from pyco.utils import disp


class BaseCommand(object):
    """A base command"""

    __metaclass__ = ABCMeta

    __cmd_name__ = ''  # command name
    __cmd_ver__ = ''  # command version
    __cmd_tags__ = []  # command tags
    __hidden__ = False

    def __init__(self, options):
        self.name = self.__cmd_name__
        self.version = self.__cmd_ver__
        self.tags = self.__cmd_tags__
        self._options = options

        if not REGEX_COMMAND_NAME.match(self.name):
            raise PyCoCommandMalformedException('Malformed command name: "{0}"'.format(self.name))
        assert len(self.name) <= 15, 'Command name: "{0}" is longer than 15 char'.format(self.name)

        self._parser = self.add_args()

        # try to automatically add 'version' option if not
        # already done by the child class
        # NOTE if you get errors here maybe you want to user
        # a conflict_handler https://docs.python.org/2/library/argparse.html#conflict-handler
        try:
            self._parser.add_argument('--version',
                                      dest='version',
                                      action='store_true',
                                      help='Show version.')
        except Exception as e:
            pass

        # add epilog to the parser if not already done by the child
        # class
        if self._parser.epilog is None:
            self._parser.epilog = '{0} ({1})'.format(self.name, self.version)

        self._options, unknown_options = self._parser.parse_known_args(options)
        if unknown_options:
            disp('Unknown options: {0}'.format(', '.join(unknown_options)))

    @abstractmethod
    def add_args(self):
        """ Use argparse to add the options to your command
        """
        raise NotImplementedError('add_args() not implemented.')

    @abstractmethod
    def impl(self):
        """
        :return: an integer: 0 exited with no errors every other number
                 can be interpreted as an error code
        """
        raise NotImplementedError('run() not implemented.')

    @TimeIt()
    def run(self):
        disp('{0} {1}'.format(self.name, self.get_options()), debug=True)
        if self.get_options().version:
            disp('{0} {1}'.format(self.name, self.version))
            return 1
        return self.impl()

    def get_parser(self):
        return self._parser

    def get_options(self):
        return self._options
