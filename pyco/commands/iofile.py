# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-06-05'
"""

import argparse
import os

from datetime import datetime

from pyco.core.base_command import BaseCommand
from pyco.utils import disp


class ListFiles(BaseCommand):
    """ List the files in the folder. """
    __cmd_name__ = 'ls'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'io']

    def __init__(self, options):
        super(ListFiles, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='List files in the current directory.')
        return parser

    def impl(self):
        files = sorted(os.listdir(os.getcwd()))

        _f = [f for f in files if os.path.isfile(os.path.join(os.getcwd(), f))]
        _d = [f for f in files if os.path.isdir(os.path.join(os.getcwd(), f))]

        _l = []
        byte_size = 0
        for items in [_d, _f]:
            for item in items:
                stat = os.stat(item)
                _l.append((stat.st_gid,
                           stat.st_uid,
                           stat.st_mode,
                           datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                           stat.st_size,
                           item))
                if len(str(stat.st_size)) > byte_size:
                    byte_size = len(str(stat.st_size)) + 1

        disp('{0:<4} {1:<4} {2:<6} {3:<20} {4:<{6}} {5}'.format('GId:',
                                                                'UId:',
                                                                'Mode:',
                                                                'Date:',
                                                                'Size:',
                                                                'Name:',
                                                                byte_size))
        for gid, uid, mode, dt, size, name in _l:
            disp('{0:<4} {1:<4} {2:<6} {3:<20} {4:<{6}} {5}'.format(gid,
                                                                    uid,
                                                                    mode,
                                                                    dt,
                                                                    size,
                                                                    name,
                                                                    byte_size))
        return 0


class ChangeDirectory(BaseCommand):
    """ Change file directory. """
    __cmd_name__ = 'cd'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'io']

    def __init__(self, options):
        super(ChangeDirectory, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Change the current working directory.')
        parser.add_argument('path',
                            help='Change directory to the new path.',
                            type=str)
        return parser

    def impl(self):
        path = self.get_options().path.strip()
        if not path:
            disp('path is empty', color='red')
            return 1
        if path == '..':
            os.chdir(os.path.split(os.getcwd())[0])
            return 0
        elif path == '/':
            os.chdir('/')
            return 0
        else:
            try:
                os.chdir(os.path.abspath(path))
            except Exception as e:
                disp(e, color='red')
                return 1
        return 0


class PrintWorkingDirectory(BaseCommand):
    """ Print working directory. """
    __cmd_name__ = 'pwd'
    __cmd_ver__ = '0.0.0'
    __cmd_tags__ = ['base', 'io']

    def __init__(self, options):
        super(PrintWorkingDirectory, self).__init__(options=options)

    def add_args(self):
        parser = argparse.ArgumentParser(prog=self.name,
                                         description='Print the current working directory.')
        return parser

    def impl(self):
        disp(os.getcwd())
        return 0
