# -*- coding: utf-8 -*-
"""
@name:          find_fold_points.py
@vers:          0.1
@author:        Douglas Thor
@created:       Sun Jun 29 17:03:12 2014
@modified:      Sun Jun 29 17:03:12 2014
@descr:         Returns the fold points - where code gets indented and
                dedented - of a .py file.
"""

from __future__ import print_function, division
import os.path
import tokenize
from StringIO import StringIO


def find_fold_points(block):
    """
    Returns a list of (start_row, end_row, indent) tuples that denote fold
    locations. Basically anywhere that there's an indent.
    """
    token_whitelist = (tokenize.NL,
                       tokenize.NEWLINE,
                       tokenize.INDENT,
                       tokenize.DEDENT,
                       tokenize.COMMENT,
                       )

    # temporary code that allows for running a block or a full file
    if os.path.isfile(block):
        with open(block) as open_file:
            token_block = tokenize.generate_tokens(open_file)
    else:
        token_block = tokenize.generate_tokens(StringIO(block).readline)

    indent_level = 0
    nl_counter = 0
    comment_counter = 0
    indents = []
    result = []
    for toknum, _, srowcol, _, _ in token_block:
        # Account for comments at the start of a block and newlines at the
        # end of a block.
        if toknum == tokenize.NL:
            nl_counter += 1
        if toknum == tokenize.COMMENT:
            comment_counter += 1
        if toknum == tokenize.INDENT:
            indent_level += 1
            indents.append(srowcol[0] - 1 - comment_counter)
        if toknum == tokenize.DEDENT:
            # the next DEDENT belongs to the most recent INDENT, so we pop off
            # the last indent from the stack
            indent_level -= 1
            matched_indent = indents.pop()
            result.append((matched_indent,
                           srowcol[0] - 1 - nl_counter,
                           indent_level + 1))
        if toknum not in token_whitelist:
            nl_counter = 0
            comment_counter = 0

    if len(indents) != 0:
        raise ValueError("Number of DEDENTs does not match number of INDENTs.")

    return result


if __name__ == "__main__":
    pass
