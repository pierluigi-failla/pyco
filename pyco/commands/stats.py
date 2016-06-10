# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-06-02'
"""

import argparse

from math import sqrt

from pyco.core.base_command import BaseCommand
from pyco.utils import disp


def mean(values):
    return float(sum(values))/len(values)


def variance(values):
    m = mean(values)
    return mean([(m - v) ** 2 for v in values])


class Stats(BaseCommand):
    """ Compute stats. """
    __cmd_name__ = 'stats'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['math', 'stats']

    def __init__(self, options):
        super(Stats, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Compute: mean (m), variance (v) and std (s) of a list of values.')
        parser.add_argument('values',
                            nargs='*',
                            type=str,
                            default=None,
                            help='The values.')
        parser.add_argument('-m', '--mean',
                            dest='mean',
                            action='store_true',
                            help='Compute only the mean.')
        parser.add_argument('-v', '--var',
                            dest='var',
                            action='store_true',
                            help='Compute only the variance.')
        parser.add_argument('-s', '--std',
                            dest='std',
                            action='store_true',
                            help='Compute only the standard deviation.')
        return parser

    def impl(self):
        if not self.get_options().values:
            return 1

        def get_values(values):
            res = []
            for v in values:
                for num in v.split(','):
                    num = num.strip()
                    if num:
                        res.append(num)
            return res

        values = get_values(self.get_options().values)
        for v in values:
            try:
                values.append(float(v))
            except Exception as e:
                disp('Value: "{0}" is not a valid number'.format(v), color='red')
        # TODO sooner or later we will add numpy (if we found a painless way of adding it)
        if self.get_options().mean:
            disp('{0}'.format(mean(values)))
            return 0
        if self.get_options().var:
            disp('{0}'.format(variance(values)))
            return 0
        if self.get_options().std:
            disp('{0}'.format(sqrt(variance(values))))
            return 0
        disp('m: {0}'.format(mean(values)))
        disp('v: {0}'.format(variance(values)))
        disp('s: {0}'.format(sqrt(variance(values))))
        return 0
