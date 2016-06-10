# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-13'
"""

import ushlex


class CommandParser(object):
    """ A stupid parse that only split the input command line in parts
    """

    _specials = [
        '>',   # redirect append 'ab'
        '>>',  # redirect new file 'wb'
        '&',   # a & b execute a and then b
        '&&',  # a && b execute a and b iff a returned 0
        '|',   # pipe to the following command
        '||',  # pipe to the following command if the previous returned 0
    ]

    def __init__(self):
        pass

    @staticmethod
    def parse(command_string):

        def f(cmd):
            if not cmd:
                return None, []
            if len(cmd) == 1:
                return cmd[0], []
            return cmd[0], cmd[1:]

        if not command_string:
            return [None, []]
        cmds = []
        cmd = []
        parts = ushlex.split(command_string)
        parts.reverse()
        special = False
        while len(parts) > 0:
            part = parts.pop()
            if part in CommandParser._specials:
                if part == '>':
                    special = True
                    filename = None
                    if len(parts) >= 1:
                        filename = parts.pop()
                    cmds.append(('rstdout', ['-f', filename, '-m', 'ab']))
                    cmds.append((f(cmd)))
                    cmds.append(('rstdout', ['-r']))
                    cmd = []
                elif part == '>>':
                    special = True
                    filename = None
                    if len(parts) >= 1:
                        filename = parts.pop()
                    cmds.append(('rstdout', ['-f', filename, '-m', 'wb']))
                    cmds.append((f(cmd)))
                    cmds.append(('rstdout', ['-r']))
                    cmd = []
                elif part == '&':
                    special = True
                    cmds.append(('var', ['-n', 'pyco_unconditional_execution', '-v', 'True']))
                    cmds.append((f(cmd)))
                    cmds.append(('var', ['-u', 'pyco_unconditional_execution']))
                    cmd = []
                elif part == '&&':
                    special = True
                    cmds.append((f(cmd)))
                    cmd = []
                elif part == '|':
                    special = True
                    cmds.append(('var', ['-n', 'pyco_unconditional_execution', '-v', 'True']))
                    cmds.append(('rstdout', ['-b']))
                    cmds.append((f(cmd)))
                    cmds.append(('rstdout', ['-r']))
                    cmds.append(('var', ['-u', 'pyco_unconditional_execution']))
                    cmd = []
                elif part == '||':
                    special = True
                    cmds.append(('rstdout', ['-b']))
                    cmds.append((f(cmd)))
                    cmds.append(('rstdout', ['-r']))
                    cmd = []
                else:
                    cmds.append((f(cmd)))
                    cmd = []
            else:
                cmd.append(part)
        if cmd:
            cmds.append((f(cmd)))
        cmds = [(cmd_name, cmd_opts) for cmd_name, cmd_opts in cmds if cmd_name is not None]

        # HACK to compute duration on the entire set of commands but I really do not like this!
        # if special and GlobalVariables.get_instance().get('timeit_commands') == 'True':
        #     c = [('var', ['-n', 'timeit_commands', '-v', 'False']),
        #          ('time', ['--start']), ]
        #     c += cmds
        #     c.extend([
        #         ('time', ['--stop']),
        #         ('var', ['-n', 'timeit_commands', '-v', 'True']), ]
        #     )
        #     return c
        return cmds
