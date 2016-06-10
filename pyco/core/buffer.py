# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-06-01'
"""

from pyco.core.global_variables import GlobalVariables


class PycoStringBuffer(object):

    BUFFER_NAME = 'pyco_buffer'

    def __init__(self):
        GlobalVariables.get_instance().set(PycoStringBuffer.BUFFER_NAME, '', level='_internal')

    def write(self, txt):
        buf = GlobalVariables.get_instance().get(PycoStringBuffer.BUFFER_NAME, level='_internal')
        GlobalVariables.get_instance().set(PycoStringBuffer.BUFFER_NAME, buf + txt, level='_internal')

    @staticmethod
    def get():
        return GlobalVariables.get_instance().get(PycoStringBuffer.BUFFER_NAME, level='_internal')
