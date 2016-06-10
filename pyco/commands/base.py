# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-15'

Few basic commands.
"""

import argparse
import os
import sys
import time

from collections import defaultdict
from datetime import datetime
from operator import itemgetter

from pyco.core.base_command import BaseCommand
from pyco.core.exceptions import PyCoQuitException
from pyco.core.global_variables import GlobalVariables
from pyco.core.history import History as Hist
from pyco.core.stdout_redirect import StdoutRedirect
from pyco.utils import disp
from pyco.utils import tail
from pyco.version import __version__ as pyco_ver


class Alias(BaseCommand):
    """Create a temporary alias for a command"""
    __cmd_name__ = 'alias'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base']

    def __init__(self, options):
        super(Alias, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Create an alias for an existing command.',
                                         usage='alias [alias name] \'[command + options]\'')
        parser.add_argument('name',
                            help='The name for the alias.',
                            type=str)
        parser.add_argument('command',
                            help='The command to be aliased.',
                            type=str)
        return parser

    def impl(self):
        # import here to avoid circular deps
        from pyco.core.parser import CommandParser
        from pyco.core.resolver import CommandResolver

        alias = self.get_options().name
        cmd_name, options = CommandParser.parse(self.get_options().command)
        disp('{0}, {1}, {2}'.format(alias, cmd_name, options))
        cmd_class, _, _ = CommandResolver.get_instance().resolve(cmd_name)
        if cmd_class is None:
            disp('Invalid alias: "{0}" is unknown.'.format(cmd_name), color='red')
            return 1
        CommandResolver.get_instance().add(alias, cmd_class, options)
        return 0


class Cat(BaseCommand):
    """ Echo function. """
    __cmd_name__ = 'cat'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'io']

    def __init__(self, options):
        super(Cat, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='The easy way of showing the file content.')

        parser.add_argument('file',
                            help='The file to cat.',
                            type=str)
        return parser

    def impl(self):
        try:
            with open(os.path.abspath(self.get_options().file), 'rb') as fin:
                for line in fin.readlines():
                    disp(line, end='')
        except Exception as e:
            disp('Exception: {0}'.format(sys.exc_info()[0]), color='red')
            return 1
        return 0


class Echo(BaseCommand):
    """ Echo function. """
    __cmd_name__ = 'echo'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base']

    def __init__(self, options):
        super(Echo, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Echo.')
        parser.add_argument('echo',
                            help='The text to be echoed.',
                            nargs='*',
                            type=str)
        return parser

    def impl(self):
        disp(' '.join(self.get_options().echo))
        return 0


class Exit(BaseCommand):
    """ Exit PyCo. """
    __cmd_name__ = 'exit'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'pyco']

    def __init__(self, options):
        super(Exit, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Exit PyCo.')
        return parser

    def impl(self):
        raise PyCoQuitException('exit')


class GlobalVariable(BaseCommand):
    """ Set global variable. """
    __cmd_name__ = 'var'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'pyco']

    def __init__(self, options):
        super(GlobalVariable, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Set and unset global variable.')
        parser.add_argument('-u', '--unset',
                            dest='unset',
                            help='Unset a given global variable.')
        parser.add_argument('-e', '--echo',
                            dest='echo',
                            help='Echo a given global variable.')
        parser.add_argument('-n', '--name',
                            dest='name',
                            help='Global variable name.')
        parser.add_argument('-v', '--value',
                            dest='value',
                            nargs='*',
                            default=None,
                            help='Global variable value.')
        parser.add_argument('-l', '--list',
                            dest='list',
                            action='store_true',
                            help='Echo all global variables.')
        return parser

    def impl(self):
        if self.get_options().list:
            name, value = GlobalVariables.get_instance().get_all()
            spacing = len(max(name, key=len))
            disp('{0: <{1}}   {2}'.format('Name:', spacing, 'Value:'))
            for n, v in sorted(zip(name, value)):
                disp('{0: <{1}} = {2}'.format(n, spacing, v))
            return 0
        if self.get_options().echo is not None:
            disp(GlobalVariables.get_instance().get(self.get_options().echo))
            return 0
        if self.get_options().unset is not None:
            GlobalVariables.get_instance().unset(self.get_options().unset)
            return 0
        else:
            GlobalVariables.get_instance().set(self.get_options().name, ' '.join(self.get_options().value))
            # disp('{0} = {1}'.format(self.get_options().name, GlobalVariables.get_instance().get(self.get_options().name)))  # noqa
        return 0


class Head(BaseCommand):
    """ Echo function. """
    __cmd_name__ = 'head'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'io']

    def __init__(self, options):
        super(Head, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Head the file.')
        parser.add_argument('-n', '--nlines',
                            dest='n',
                            default=10,
                            help='Number of lines to show, (default=%(default)r).',
                            type=int)
        parser.add_argument('-r', '--reverse',
                            dest='r',
                            action='store_true',
                            help='Reverse the line order, (default=%(default)r).')
        parser.add_argument('file',
                            help='The file to head.',
                            type=str)
        return parser

    def impl(self):
        try:
            with open(os.path.abspath(self.get_options().file), 'rb') as fin:
                lines = fin.readlines()[:self.get_options().n]
                if self.get_options().r:
                    lines = lines.reverse()
                for line in lines:
                    disp(line, end='')
        except Exception as e:
            disp('Exception: {0}'.format(sys.exc_info()[0]), color='red')
            return 1
        return 0


class Help(BaseCommand):
    """ Show PyCo Help. """
    __cmd_name__ = 'help'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'pyco']

    HELP = """
Welcome to PyCo {0}

PyCo is a Python console that allows you to build your own
commands and interact with the system in a bash-fashion.

TODO: maybe this could be improved
""".format(pyco_ver)

    def __init__(self, options):
        super(Help, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Show PyCo help.')
        return parser

    def impl(self):
        disp(self.HELP)
        return 0


class History(BaseCommand):
    """Show and interact with the history file."""
    __cmd_name__ = 'history'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'pyco']

    def __init__(self, options):
        super(History, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Show the history or search there.')
        parser.add_argument('-s', '--search',
                            dest='search',
                            nargs='*',
                            default=None,
                            type=str,
                            help='Search in the history.')
        parser.add_argument('-d', '--delete',
                            dest='delete',
                            action='store_true',
                            help='Delete the history.')
        return parser

    def impl(self):
        if self.get_options().delete:
            Hist.get_instance().delete()
            disp('History deleted.')
            return 0
        try:
            lines = Hist.get_instance().read()
            search = self.get_options().search
            if search:
                disp('Searching for: "{0}"'.format(' '.join(search)))
                unique_lines = defaultdict(float)
                for line in lines:
                    if line not in unique_lines and not line.startswith('history'):
                        score = 0.0
                        for part in search:
                            if part in line:
                                score += 1.0
                        unique_lines[line] = score / float(max(len(line.split(' ')), len(search)))
                del lines  # free some memory
                top_lines = sorted(unique_lines.items(), key=itemgetter(1), reverse=True)[:5]
                if not top_lines:
                    disp('Not found...')
                    return 0
                for line, score in top_lines:
                    disp('{0:.2f}\t{1}'.format(score, line))
                disp('...')
            else:
                for line in lines:
                    disp(line)
        except Exception as e:
            disp('Exception: {0}'.format(sys.exc_info()[0]), color='red')
            return 1
        return 0


class ListCommands(BaseCommand):
    """Show all available commands."""
    __cmd_name__ = 'list'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'pyco']

    def __init__(self, options):
        super(ListCommands, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Show all available commands.')
        parser.add_argument('-r', '--reverse',
                            dest='r',
                            action='store_true',
                            help='Sort ascending, (default=%(default)r).')
        return parser

    def impl(self):
        # import here to avoid circular deps
        from pyco.core.resolver import CommandResolver

        reverse = self.get_options().r
        commands_list = CommandResolver.get_instance().get_command_names_and_details()
        disp('{0: <16}{1}'.format('Name:', 'Tags:'))
        for command, tags, hidden in sorted(commands_list, key=lambda tup: tup[0], reverse=reverse):
            if not hidden:
                disp('{0: <16}{1}'.format(command, ','.join(sorted(tags))))
        return 0


class RedirectStdout(BaseCommand):
    """Show all available commands."""
    __cmd_name__ = 'rstdout'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'pyco']
    __hidden__ = True  # this command is not intended to be used directly

    def __init__(self, options):
        super(RedirectStdout, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Redirect stdout to file or back to console.')

        parser.add_argument('-f', '--file',
                            dest='file',
                            help='The file to redirect to.',
                            nargs='?')
        parser.add_argument('-m', '--mode',
                            dest='mode',
                            help='The mode to open the file: write wb or append ab, (default=%(default)r).',
                            nargs='?',
                            default='wb')
        parser.add_argument('-b', '--buffer',
                            dest='buffer',
                            help='Redirect stdout and stderr to an internal buffer.',
                            nargs='?')
        parser.add_argument('-r', '--reset',
                            dest='reset',
                            action='store_true',
                            help='Reset the stdout to console.')
        return parser

    def impl(self):
        if self.get_options().reset:
            StdoutRedirect.get_instance().reset()
            return 0
        if self.get_options().mode and self.get_options().file:
            if self.get_options().mode not in ['wb', 'ab']:
                disp('Value: "{0}" is not valid for argument --mode.'.format(self.get_options().mode))
                return 1
            if not self.get_options().file:
                disp('Filename: "{0}" is not valid for argument --file.'.format(self.get_options().file))
                return 1
            StdoutRedirect.get_instance().to_file(os.path.abspath(self.get_options().file),
                                                  mode=self.get_options().mode)
            return 0
        if self.get_options().buffer:
            print('to_buffer')
            StdoutRedirect.get_instance().to_buffer()
        return 0


class Tail(BaseCommand):
    """ Show current date and time. """
    __cmd_name__ = 'tail'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'io']

    def __init__(self, options):
        super(Tail, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Show the content of file by the end.')
        parser.add_argument('-n', '--nlines',
                            dest='n',
                            default=10,
                            help='Number of lines to show, (default=%(default)r).',
                            type=int)
        parser.add_argument('-r', '--reverse',
                            dest='r',
                            action='store_true',
                            help='Reverse the line order.')
        parser.add_argument('file',
                            help='The file to be shown.',
                            type=argparse.FileType('rb'))
        return parser

    def impl(self):
        try:
            with open(os.path.abspath(self.get_options().file), 'rb') as fin:
                lines = tail(fin, lines=self.get_options().n).split('\n')
                if self.get_options().r:
                    lines = lines.reverse()
                for line in lines:
                    disp(line)
        except Exception as e:
            disp('Exception: {0}'.format(sys.exc_info()[0]), color='red')
            return 1
        return 0


class Time(BaseCommand):
    """ Show current date and time. """
    __cmd_name__ = 'time'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'pyco']

    GLOBAL_VAR_NAME = 'pyco_internal_timer'  # this is an internal global variable

    def __init__(self, options):
        super(Time, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Show current date and time.')
        parser.add_argument('--start',
                            dest='start',
                            action='store_true',
                            help='Start the timer.')
        parser.add_argument('--stop',
                            dest='stop',
                            action='store_true',
                            help='Stop the timer.')
        return parser

    def impl(self):
        if self.get_options().start:
            GlobalVariables.get_instance().set(Time.GLOBAL_VAR_NAME, time.time(), level='_internal')
            return 0
        if self.get_options().stop:
            delta = time.time() - GlobalVariables.get_instance().get(Time.GLOBAL_VAR_NAME, level='_internal')
            disp('Elapsed time: {0:.3f} secs ='.format(delta))
            return 0
        disp(datetime.now().strftime('%A %Y-%m-%d %H:%M:%S.%f %Z'))
        return 0
