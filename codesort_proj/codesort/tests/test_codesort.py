# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 16:26:08 2014

@name:          test_codesort.py
@vers:          0.1
@author:        dthor
@created:       Wed Jun 18 16:26:08 2014
@modified:      Wed Jun 18 16:26:08 2014
@descr:         Unit Testing for codesort.codesort module
"""

from __future__ import print_function, division
import unittest
import os
import codesort.codesort as codesort


# Module constants used in most test cases
DATA_PATH = os.path.join(os.path.split(__file__)[0], 'test_data')
SORTED_TEST_FILES = ["sorted_1.py",
                     ]
UNSORTED_TEST_FILES = ["unsorted_1.py",
                       ]
SORTED_TEST_PATHS = [os.path.join(DATA_PATH, x) for x in SORTED_TEST_FILES]
UNSORTED_TEST_PATHS = [os.path.join(DATA_PATH, x) for x in UNSORTED_TEST_FILES]


class CodeSort(unittest.TestCase):
    """ Unit Testing """
    def setUp(self):
        self.path = r"X:\WinPython27\projects\codesort\tests\test_data"
        self.filenames = (("unsorted_1.py", "sorted_1.py"),
                          )
        self.known_values = []
        for test_file, ref_file in self.filenames:
            self.known_values.append((os.path.join(self.path, test_file),
                                      os.path.join(self.path, ref_file)))

    def test_known_values(self):
        """
        KVT for CodeSort: verify that the sorted test file matches
        with the reference file.
        """

        for test_file, ref_file in self.known_values:
#            result = codesort(test_file, True)
#            self.assertTrue(codesort.binary_file_compare(result, ref_file))
#            print(self.known_values)
            continue


class CodeBlockKnownValues(unittest.TestCase):
    """ Unit Testing for the CodeBlock class"""
    chunk_1 = """class HelloKitty(object):
    def __init__(self):
        pass

    def method(self):
        return 5"""

    chunk_2 = """def my_function(a, b):
        return a + b"""

    # (chunk, (name, type, num_lines))
    known_values = ((chunk_1, ("HelloKitty", 'class', 6)),
                    (chunk_2, ("my_function", 'function', 2)),
                    )

    def test_kvt_name(self):
        """ Known-value testing for the CodeBlock name attribute. """
        for chunk, expected in self.known_values:
            result_obj = codesort.CodeBlock(chunk)
            self.assertEqual(expected[0], result_obj.name)

    def test_kvt_type(self):
        """ Known-value testing for the CodeBlock type attribute. """
        for chunk, expected in self.known_values:
            result_obj = codesort.CodeBlock(chunk)
            self.assertEqual(expected[1], result_obj.code_type)

    def test_kvt_line_count(self):
        """ Known-value testing for the CodeBlock line_count attribute. """
        for chunk, expected in self.known_values:
            result_obj = codesort.CodeBlock(chunk)
            self.assertEqual(expected[2], result_obj.line_count)


class ClassifyBlock(unittest.TestCase):
    """ Unit testing for the classify_block function """
    ex1 = ('class Apple(object):', 'class')
    ex2 = ('   def my_func(a, b):', 'function')
    ex3 = ('y = 4x', 'instance_var')
    ex4 = ("""    @decorator1
    @decorator2
    def my_decorated_function(b, c):)""", 'function')
    ex5 = ('# a comment', 'comment')
    ex6 = ('from module import thing', 'import')
    ex7 = ('import other_module', 'import')
    ex8 = ('""" A docstring """', 'docstring')
    ex9 = ('CONSTANT = 57', 'constant')

    examples = [ex1,
                ex2,
                ex3,
                ex4,
                ex5,
                ex6,
                ex7,
                ex8,
                ex9,
                ]

    def test_known_values(self):
        """ Known-value testing for the classify_block function """
        for block, expected in self.examples:
            code_type = codesort.classify_block(block)
            self.assertEqual(code_type, expected)

    def test_constant_match(self):
        """ Makes sure that constants that match PEP8 standards will work """
        blocks = ['CONSTANT = "helloooo, nurse!"',
                  'SOME_CONSTANT = 57',
                  '99_PROBLEMS = "but a bug aint one!"',
                  'CONST_1 = 2',
                  ]

        for block in blocks:
            self.assertEqual(codesort.classify_block(block), 'constant')

    def test_constant_not_match(self):
        """ Test that some common invalid constants are not matched """
        blocks = ['Constant=[x for x in range(5)]',
                  'con=2',
                  'AAA=-11',
                  ]

        for block in blocks:
            self.assertNotEqual(codesort.classify_block(block), 'constant')


#class SplitIntoBlocks(unittest.TestCase):
#    """ Unit Testing for the split_into_blocks function.
#    Consider renaming to block_split or split_blocks """
#    # Test Block file is located in .../test_data/split_blocks.
#    test1 = ("""def myfunc(a, b):
#    if a < 0:
#        return b
#    if a > 0:
#        return a + b
#    return 0
#
#def myfunc2(a):
#    return 'xsdfsd' + (a-2)*(a+3)""", [(1, 7), (8, 9)])
#    test2 = ("""def func1(a):
#    return a
#
#def func2(b):
#    return b
#
#def func3(c):
#    return c""", [(1, 3), (4, 6), (7, 8)])
#
#    test3 = ("""import apples
#
#def myfunc(a, b):
#    if a < 0:
#        return b
#    if a > 0:
#        return a + b
#    return 0
#
#def myfunc2(a):
#    return 'xsdfsd' + (a-2)*(a+3)""", [(3, 9), (10, 11)])
#    known_values = (test1,
#                    test2,
#                    test3,
#                    )
#
#    def test_known_values(self):
#        """ KVT """
#        for code_block, expected in self.known_values:
#            result = codesort.split_into_blocks(code_block)
#            self.assertEqual(result, expected)


class FindFoldPoints(unittest.TestCase):
    """ testing the find_folds function """
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

    root_dir = os.getcwd()
    test_data_path = r"codesort\\tests\\test_data"
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
            result = codesort.find_fold_points(code_block)
            self.assertSetEqual(set(result), folds)

    def test_known_file(self):
        with open(self.file_1) as openfile:
            file_text = "".join(openfile.readlines())
        result = codesort.find_fold_points(file_text)
        self.assertSetEqual(set(result), self.file_1_result)


class SplitBlocks(unittest.TestCase):
    """ doc """
    def test_known_values(self):
        """ doc """
        for path in SORTED_TEST_PATHS:
            with open(path) as openfile:
                file_text = "".join(openfile.readlines())
            try:
                # TODO: remove dependence on find_fold_points
                #   (This currently tests two things which is a no-no.)
                codesort.split_blocks(file_text,
                                      codesort.find_fold_points(file_text))
                passed = True
            except:
                passed = False
            self.assertTrue(passed)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=1)
