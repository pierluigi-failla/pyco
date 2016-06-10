# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-06-01'
"""

import sys

from pyco.core.buffer import PycoStringBuffer


class StdoutRedirect(object):

    _instance = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if StdoutRedirect._instance is None:
            StdoutRedirect._instance = StdoutRedirect()
        return StdoutRedirect._instance

    @staticmethod
    def to_file(file_name, mode='wb'):
        """This will redirect stdout and stderr to a file."""
        _file = open(file_name, mode)
        sys.stdout = _file
        sys.stderr = _file

    @staticmethod
    def to_buffer():
        """This will store the output in an internal global variable."""
        _buf = PycoStringBuffer()
        sys.stdout = _buf
        sys.stderr = _buf

    @staticmethod
    def get_buffer():
        return PycoStringBuffer.get()

    @staticmethod
    def reset():
        """Reset stdout and stderr"""
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__