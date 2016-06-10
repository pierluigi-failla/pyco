# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-12'
"""

import sys

from setuptools import setup
from setuptools import find_packages
from sys import platform

from pyco.version import __version__

exec (open('pyco/version.py').read())

if platform == 'win32':
    # win
    import py2exe
    sys.argv.append('py2exe')
elif platform == "linux" or platform == "linux2":
    # linux
    pass
elif platform == "darwin":
    # osx
    pass

data_files = [('.', [
    'pyco/.config',
    'pyco/.aliases',
])]

setup(
    name='PyCo',
    version=__version__,
    author='Pierluigi Failla',
    description='PyCo - The Python Console',
    install_requires=['pyco'],
    packages=find_packages(),
    console=['pyco/pyconsole.py'],
    data_files=data_files,
    options={
        'py2exe':
            {
                'bundle_files': 1,
                'optimize': 2,
                'unbuffered': True,
            }
    },
)
