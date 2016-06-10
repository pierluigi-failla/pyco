# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-17'
"""


class GlobalVariables(object):
    """ A singleton for the Global Environment

    This class takes care of collecting global variables
    and settings. All global variables are assumed to be
    strings.
    """

    _instance = None
    _data = {
        '_public': {},
        '_internal': {}
    }

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if GlobalVariables._instance is None:
            GlobalVariables._instance = GlobalVariables()
        return GlobalVariables._instance

    @staticmethod
    def get(name, level='_public'):
        return GlobalVariables._data[level].get(name, None)

    @staticmethod
    def get_all(level='_public'):
        return GlobalVariables._data[level].keys(), GlobalVariables._data[level].values()

    @staticmethod
    def set(name, value, level='_public'):
        GlobalVariables._data[level][name] = value

    @staticmethod
    def unset(name, level='_public'):
        GlobalVariables._data[level][name] = None

    @staticmethod
    def remove(name, level='_public'):
        del GlobalVariables._data[level][name]


