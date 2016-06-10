# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-12'
"""

from pyco.core.buffer import PycoStringBuffer
from pyco.core.loaders import AliasLoader
from pyco.core.loaders import ConfigLoader
from pyco.core.exceptions import PyCoQuitException
from pyco.core.global_variables import GlobalVariables
from pyco.core.history import History
from pyco.core.prompt import Prompt
from pyco.core.resolver import CommandResolver
from pyco.utils import disp
from pyco.initialize import get_input

_GV_ = GlobalVariables.get_instance()


def main():

    command_resolver = CommandResolver.get_instance()
    history = History.get_instance()

    disp('Loading config...')
    try:
        ConfigLoader('.config')
    except Exception as e:
        disp('ConfigLoader: {0}'.format(e), color='red')

    disp('Loading aliases...')
    try:
        AliasLoader()
    except Exception as e:
        disp('AliasLoader: {0}'.format(e), color='red')

    infinite_loop = True
    while infinite_loop:
        disp(Prompt().show(), color='blue', end='')
        command_str = get_input().strip()
        if not command_str:
            continue
        history.append(command_str)
        command_pipe = command_resolver.resolve(command_str)
        for cmd_class, options, suggested_cmd in command_pipe:
            disp('cmd_class: {0} options: {1} suggested_cmd: {2}'.format(cmd_class, options, suggested_cmd), debug=True)
            if cmd_class is not None:
                try:
                    # if the PycoStringBuffer is not empty means that | or ||
                    # has been used
                    if PycoStringBuffer.get() and len(command_pipe) > 1:
                        options.append(PycoStringBuffer.get())
                    r = cmd_class(options).run()
                    if r != 0:
                        disp('Command "{0}" finished with exit code: {1}'.format(cmd_class.__cmd_name__, r),
                             color='red')

                        # see parser '&' definition
                        if _GV_.get('pyco_unconditional_execution') == 'True':
                            continue
                        break
                except (KeyboardInterrupt, SystemExit) as e:
                    pass
                except PyCoQuitException as e:
                    disp('Exiting...')
                    infinite_loop = False
                    break
                except Exception as e:
                    disp('Exception "{0}": {1}'.format(cmd_class.__cmd_name__, e), color='red')
            else:
                disp('Command "{0}" not found.'.format(command_str.split(' ')[0]))
                if suggested_cmd is not None:
                    disp('Did you mean: "{0}"?'.format(suggested_cmd), color='red')
    return 0

if __name__ == '__main__':
    main()
