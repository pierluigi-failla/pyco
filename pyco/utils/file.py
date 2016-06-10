# -*- coding: utf-8 -*-
"""
author = 'Pierluigi'
date = '2016-05-19'
"""


def tail(f, lines=20):
    """Native python tail implementation

    Adapted from: http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail

    :param f: a file
    :param lines: number of line to return
    :return: a string containing the required lines
    """
    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = lines
    block_number = -1
    blocks = []  # blocks of size BLOCK_SIZE, in reverse order starting
    # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if block_end_byte - BLOCK_SIZE > 0:
            # read the last block we haven't yet read
            f.seek(block_number * BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0, 0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-lines:])
