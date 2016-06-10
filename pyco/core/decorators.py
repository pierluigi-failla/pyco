# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-17'
"""

import time

from pyco.core.global_variables import GlobalVariables
from pyco.utils import disp


class TimeIt(object):
    """A decorator to measure the time spent by a function"""

    def __init__(self):
        pass

    def __call__(self, f):
        def wrapped_f(*args):
            if GlobalVariables.get_instance().get('timeit_commands') != 'True':
                return f(*args)
            ts = time.time()
            r = f(*args)
            te = time.time()
            disp('\n= Executed in {0:.3f} secs ='.format(te-ts), color='yellow')
            return r
        return wrapped_f
