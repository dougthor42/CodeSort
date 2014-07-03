# -*- coding: utf-8 -*-
"""
@name:          find_fold_points.py
@vers:          0.1
@author:        Douglas Thor
@created:       Sun Jun 29 17:03:12 2014
@modified:      Sun Jun 29 17:03:12 2014
@descr:         A distributable version of the find_fold_points function
                Has built-in unit testing for easier distribution.
"""

from __future__ import print_function, division
import unittest
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

#
#class TestFindFoldPoints(unittest.TestCase):
#    """ Test the find_fold_points function """
#    root_dir = os.path.split(__file__)[0]
#    test_data_path = r"tests\test_data"
#    file_1 = "sorted_1.py"
#    file_2 = "2_multiline_defs.py"
#    file_3 = "3_comments.py"
#    file_1_path = os.path.join(root_dir, test_data_path, file_1)
#    file_2_path = os.path.join(root_dir, test_data_path, file_2)
#    file_3_path = os.path.join(root_dir, test_data_path, file_3)
#
#    # Manually determined the (start, end, indent) values for the file
#    file_1_result = {(10, 34, 1),
#                     (12, 14, 2),
#                     (16, 18, 2),
#                     (20, 22, 2),
#                     (24, 26, 2),
#                     (28, 30, 2),
#                     (32, 34, 2),
#                     (37, 61, 1),
#                     (39, 41, 2),
#                     (43, 45, 2),
#                     (47, 49, 2),
#                     (51, 53, 2),
#                     (55, 57, 2),
#                     (59, 61, 2),
#                     (64, 66, 1),
#                     (69, 71, 1),
#                     (74, 76, 1),
#                     (79, 81, 1),
#                     }
#
#    file_2_result = {(10, 40, 1),
#                     (14, 16, 2),
#                     (22, 24, 2),
#                     (30, 32, 2),
#                     (38, 40, 2),
#                     }
#
#    file_3_result = {(10, 35, 1),
#                     (14, 16, 2),
#                     (22, 24, 2),
#                     (26, 29, 2),
#                     (31, 35, 2),
#                     }
#
#    def test_known_file(self):
#        """ Run find_fold_points a on known file. """
#        with open(self.file_1_path) as openfile:
#            file_text = "".join(openfile.readlines())
#        result = find_fold_points(file_text)
#        self.assertSetEqual(set(result), self.file_1_result)
#
#    def test_multiline_defs(self):
#        """ Make sure multiline definitions are folded after the : """
#        with open(self.file_2_path) as openfile:
#            file_text = "".join(openfile.readlines())
#        result = find_fold_points(file_text)
#        self.assertSetEqual(set(result), self.file_2_result)
#
#    def test_comment_after_def(self):
#        """ Check that comments after fold start are properly folded """
#        with open(self.file_3_path) as openfile:
#            file_text = "".join(openfile.readlines())
#        result = find_fold_points(file_text)
#        self.assertSetEqual(set(result), self.file_3_result)


if __name__ == "__main__":
#    unittest.main(exit=False, verbosity=2)
    pass
