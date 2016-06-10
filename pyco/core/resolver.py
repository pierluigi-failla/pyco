# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-13'
"""

from inspect import getmembers
from inspect import getmro
from inspect import isclass

import pyco.commands as commands

from pyco.core.parser import CommandParser
from pyco.utils import disp
from pyco.utils import levenshtein


class CommandResolver(object):
    """ A singleton basic command resolver

    This class takes care of resolving commands to BaseCommand classes
    and solve aliases.
    """
    _instance = None
    _command_map = {}
    _calls = 0

    def __init__(self):
        CommandResolver._calls = 0
        for _, klass in getmembers(commands):
            if isclass(klass) and getmro(klass)[1].__name__ == 'BaseCommand':
                CommandResolver.add(klass.__cmd_name__, klass, [])
        CommandResolver._command_names = sorted(CommandResolver._command_map.keys())

    @staticmethod
    def get_instance():
        if CommandResolver._instance is None:
            CommandResolver._instance = CommandResolver()
        return CommandResolver._instance

    @staticmethod
    def add(command_name, command_class, command_options):
        if command_name in CommandResolver._command_map:
            disp('Command "{0}" has been overridden by class "{1}"'.format(command_name, command_class.__name__),
                 color='red')
        CommandResolver._command_map[command_name] = (command_class, command_options)

    @staticmethod
    def get_class(command_name):
        return CommandResolver._command_map[command_name]

    @staticmethod
    def resolve(command_str):
        """
        :param command_str: the command or alias name
        :return: I list of tuple:
                 - cmd_class: the class that implements the command
                 - add_opts: if the command is an alias, some additional options
                             needs to be forwards to the run()
                 - suggested_cmd: if the command_name cannot be found I try to
                                  suggest one
        """
        CommandResolver._calls += 1
        # parse will return the name and the options provided by the user
        cmds = []
        for cmd_name, options in CommandParser.parse(command_str):
            # get the command class and add_opts (if the command is an alias could have additional options)
            cmd_class, add_opts = CommandResolver._command_map.get(cmd_name, (None, []))
            suggested_cmd = None
            if cmd_class is None:
                suggested_cmd = CommandResolver.suggest_command(cmd_name)
            cmds.append((cmd_class, add_opts + options, suggested_cmd))
        return cmds

    @staticmethod
    def get_command_names():
        return sorted(CommandResolver._command_map.keys())

    @staticmethod
    def get_command_names_and_details():
        """This will return a list of command names and tags"""
        lst = []
        for cmd_name, (klass, _) in CommandResolver._command_map.iteritems():
            lst.append((cmd_name, klass.__cmd_tags__, klass.__hidden__))
        return sorted(lst, key=lambda tup: tup[0])

    @staticmethod
    def suggest_command(command_name):
        suggested_cmd = None
        best_match_value = 1000  # just a random big number
        for cmd in sorted(CommandResolver.get_command_names(), key=len):
            match_value = levenshtein(cmd, command_name)
            if match_value < best_match_value:
                best_match_value = match_value
                suggested_cmd = cmd
        return suggested_cmd
