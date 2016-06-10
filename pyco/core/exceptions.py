# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-15'
"""


class PyCoException(Exception):
    """Base class for PyCo exceptions."""
    def __init__(self, message):
        super(PyCoException, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class PyCoQuitException(PyCoException):
    """If this exception is raised PyCo will be closed."""
    def __init__(self, message):
        super(PyCoQuitException, self).__init__(message)


class PyCoCommandMalformedException(PyCoException):
    """If command is malformed."""
    def __init__(self, message):
        super(PyCoCommandMalformedException, self).__init__(message)


class PyCoLoaderException(PyCoException):
    """Raised if file loader finds something strange."""
    def __init__(self, message):
        super(PyCoLoaderException, self).__init__(message)

