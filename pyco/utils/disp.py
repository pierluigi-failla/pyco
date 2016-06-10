# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-14'
"""

from __future__ import print_function

import sys

from colorama import Fore

from pyco.core.global_variables import GlobalVariables

_colors = {
    'white': Fore.WHITE,
    'red': Fore.LIGHTRED_EX,
    'green': Fore.LIGHTGREEN_EX,
    'blue': Fore.LIGHTBLUE_EX,
    'yellow': Fore.LIGHTYELLOW_EX,
    'cyan': Fore.LIGHTCYAN_EX,
    'magenta': Fore.LIGHTMAGENTA_EX
}


def _get_pyco_debug_status():
    """Return the curret status for the PyCo debug."""
    debug = GlobalVariables.get_instance().get('debug')
    if debug is None:
        return False
    return True if debug.strip().lower() == 'true' else False


def disp(text='', color='white', end='\n', flush=False, debug=False):
    """A display function

    :param text: the text to be shown
    :param color: color for the text
    :param end: terminator
    :param flush: force flush
    :param debug: if debug is true the text is shown only if config set debug true
    """
    d = ''
    show_debug = (debug and _get_pyco_debug_status())
    if show_debug:
        d = 'DEBUG: '
    if not debug or show_debug:
        if sys.stdout != sys.__stdout__:
            print('{0}{1}'.format(d, text), end=end)
        else:
            print('{0}{1}{2}'.format(d, _colors.get(color, 'white'), text), end=end)
    if flush:
        sys.stdout.flush()
