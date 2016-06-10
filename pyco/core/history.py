# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-19'
"""

import os

from pyco.core.global_variables import GlobalVariables


class History(object):
    """This class takes care of the history

    in first instance this will collect all
    commands run by the user.
    """

    _instance = None

    @staticmethod
    def get_instance():
        if History._instance is None:
            History._instance = History()
        return History._instance

    @staticmethod
    def append(command):
        """Append the command to the history."""
        with open(GlobalVariables.get_instance().get('history_filename'), 'ab') as fin:
            fin.write('{0}\n'.format(command))
        fin.close()

    @staticmethod
    def read():
        """Read all the history and return it in a list."""
        with open(GlobalVariables.get_instance().get('history_filename'), 'rb') as fin:
            lines = []
            for line in fin.readlines():
                lines.append(line.replace('\n', '').strip())
        fin.close()
        return lines

    @staticmethod
    def delete():
        os.remove(GlobalVariables.get_instance().get('history_filename'))
