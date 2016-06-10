# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-06-04'
"""

import argparse
import pygal

from pyco.core.base_command import BaseCommand
from pyco.utils import disp


def get_values(values):
    vals = []
    for v in values:
        for num in v.split(','):
            if num.strip():
                try:
                    vals.append(float(num.strip()))
                except Exception as e:
                    disp('Value: {0} is not a valid number'.format(num), color='red')
    return vals


class Plot(BaseCommand):
    """ Show PyCo Help. """
    __cmd_name__ = 'plot'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['math', 'visualization']

    def __init__(self, options):
        super(Plot, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Plot the data using the pygal library (http://www.pygal.org/).')
        parser.add_argument('-x',
                            nargs='*',
                            type=str,
                            help='x values.')
        parser.add_argument('-y',
                            nargs='*',
                            type=str,
                            help='y values.')
        parser.add_argument('--width',
                            dest='width',
                            help='The figure width in px (default=%(default)r).',
                            default=600,
                            type=int,
                            nargs='?')
        parser.add_argument('--height',
                            dest='height',
                            help='The figure height in px (default=%(default)r).',
                            default=400,
                            type=int,
                            nargs='?')
        parser.add_argument('-b', '--browser',
                            dest='browser',
                            default=True,
                            type=bool,
                            help='Open the plot in the browser (default=%(default)r).')
        parser.add_argument('-f', '--file_name',
                            dest='file',
                            help='Save the plot to the png file.',
                            nargs='?')
        return parser

    def impl(self):
        opts = self.get_options()
        if not opts.x:
            disp('x is empty', color='red')
            return 1
        if not opts.y:
            disp('y is empty', color='red')
            return 1
        x_values = get_values(opts.x)
        y_values = get_values(opts.y)
        if len(x_values) != len(y_values):
            disp('Size mismatch: x = {0}, y = {1}'.format(len(x_values), len(y_values)), color='red')
            return 1
        chart = pygal.Line(width=opts.width, height=opts.height, explicit_size=True)
        chart.title = 'Plot'
        chart.x_labels = x_values
        chart.add('data', y_values)
        if opts.browser:
            chart.render_in_browser()
        if opts.file:
            chart.render_to_png(opts.file)
        return 0
