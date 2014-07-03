# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 17:06:51 2014

@name:          test_ffp.py
@vers:          0.1
@author:        dthor
@created:       Wed Jul 02 17:06:51 2014
@modified:      Wed Jul 02 17:06:51 2014
@descr:         Unit Testing for codesort.find_fold_points module
"""

from __future__ import print_function
import unittest
import os
import codesort.find_fold_points as ffp


class FindFoldPoints(unittest.TestCase):
    """ Test the find_fold_points function """
    root_dir = os.path.split(__file__)[0]
    test_data_path = r"test_data"
    file_1 = "sorted_1.py"
    file_2 = "2_multiline_defs.py"
    file_3 = "3_comments.py"
    file_1_path = os.path.join(root_dir, test_data_path, file_1)
    file_2_path = os.path.join(root_dir, test_data_path, file_2)
    file_3_path = os.path.join(root_dir, test_data_path, file_3)

    # Manually determined the (start, end, indent) values for the file
    file_1_result = {(10, 34, 1),
                     (12, 14, 2),
                     (16, 18, 2),
                     (20, 22, 2),
                     (24, 26, 2),
                     (28, 30, 2),
                     (32, 34, 2),
                     (37, 61, 1),
                     (39, 41, 2),
                     (43, 45, 2),
                     (47, 49, 2),
                     (51, 53, 2),
                     (55, 57, 2),
                     (59, 61, 2),
                     (64, 66, 1),
                     (69, 71, 1),
                     (74, 76, 1),
                     (79, 81, 1),
                     }

    file_2_result = {(10, 40, 1),
                     (14, 16, 2),
                     (22, 24, 2),
                     (30, 32, 2),
                     (38, 40, 2),
                     }

    file_3_result = {(10, 35, 1),
                     (14, 16, 2),
                     (22, 24, 2),
                     (26, 29, 2),
                     (31, 35, 2),
                     }

    test1 = ("""def myfunc(a, b):
    if a < 0:
        return b
    if a > 0:
        return a + b
    return 0

def myfunc2(a):
    return 'xsdfsd' + (a-2)*(a+3)""", {(1, 6, 1),
                                       (2, 3, 2),
                                       (4, 5, 2),
                                       (8, 9, 1),
                                       })

    test2 = ("""def func1(a):
    return a

def func2(b):
    return b

def func3(c):
    return c""", {(1, 2, 1),
                  (4, 5, 1),
                  (7, 8, 1),
                  })

    test3 = ("""import apples

def myfunc(a, b):
    if a < 0:
        return b
    if a > 0:
        return a + b
    return 0

def myfunc2(a):
    return 'xsdfsd' + (a-2)*(a+3)""", {(3, 8, 1),
                                       (4, 5, 2),
                                       (6, 7, 2),
                                       (10, 11, 1),
                                       })
    known_values = (test1,
                    test2,
                    test3,
                    )

    file_1_name = "sorted_1.py"
    file_1 = os.path.join(root_dir, test_data_path, file_1_name)
    file_1_result = {(10, 34, 1),
                     (12, 14, 2),
                     (16, 18, 2),
                     (20, 22, 2),
                     (24, 26, 2),
                     (28, 30, 2),
                     (32, 34, 2),
                     (37, 61, 1),
                     (39, 41, 2),
                     (43, 45, 2),
                     (47, 49, 2),
                     (51, 53, 2),
                     (55, 57, 2),
                     (59, 61, 2),
                     (64, 66, 1),
                     (69, 71, 1),
                     (74, 76, 1),
                     (79, 81, 1)}

    def test_known_values(self):
        """ docstring """
        for code_block, folds in self.known_values:
            result = ffp.find_fold_points(code_block)
            self.assertSetEqual(set(result), folds)

    def test_known_file(self):
        with open(self.file_1) as openfile:
            file_text = "".join(openfile.readlines())
        result = ffp.find_fold_points(file_text)
        self.assertSetEqual(set(result), self.file_1_result)


    def test_known_file2(self):
        """ Run find_fold_points a on known file. """
        with open(self.file_1_path) as openfile:
            file_text = "".join(openfile.readlines())
        result = ffp.find_fold_points(file_text)
        self.assertSetEqual(set(result), self.file_1_result)

    def test_multiline_defs(self):
        """ Make sure multiline definitions are folded after the : """
        with open(self.file_2_path) as openfile:
            file_text = "".join(openfile.readlines())
        result = ffp.find_fold_points(file_text)
        self.assertSetEqual(set(result), self.file_2_result)

    def test_comment_after_def(self):
        """ Check that comments after fold start are properly folded """
        with open(self.file_3_path) as openfile:
            file_text = "".join(openfile.readlines())
        result = ffp.find_fold_points(file_text)
        self.assertSetEqual(set(result), self.file_3_result)


def main():
    """ Main Code """
    unittest.main(exit=False, verbosity=1)


if __name__ == "__main__":
    main()
