# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-13'
"""

from __future__ import print_function

import os

from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime


class BasePrompt(object):
    """Abstract class for the prompt."""

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def show(self):
        raise NotImplementedError('show() not implemented.')

    @abstractmethod
    def update(self):
        raise NotImplementedError('update() not implemented.')


class Prompt(BasePrompt):
    """A class for handling the prompt."""

    def __init__(self):
        super(Prompt, self).__init__()

    def show(self):
        """Super simple prompt."""
        directory = os.path.split(os.getcwd())[1]
        if not directory:
            directory = os.path.split(os.getcwd())[0]
        return '[{0} {1}]$ '.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), directory)

    def update(self):
        pass
