# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 16:50:37 2014

@name:          codesort.py
@vers:          0.1
@author:        dthor
@created:       Wed Jun 18 16:50:37 2014
@modified:      Wed Jun 18 16:50:37 2014
@descr:         A new file

Usage:
    codesort.py
    codesort.py FILE
    codesort.py FILE [-n]

Options:
    -n --new-file       # Create a new file rather than replacing the old one.
    -h --help           # Show this screen.
    --version           # Show version.
"""


from __future__ import print_function, division
from docopt import docopt
import os.path
import string


BLOCK_TYPE = {'@': 'decorator',
              'class': 'class',
              'def': 'function',
              '#': 'comment',
              'from': 'import',
              'import': 'import',
              '"""': 'docstring',
#              set(string.ascii_uppercase): 'constant',
              }


class CodeSort(object):
    """
    Main CodeSort class

    Contains all the methods and attributes for the module.
    """
    def __init__(self, filepath):
        """ Init class attributes """
        self.filepath = filepath

    def __str__(self):
        """ String representation """
        return "CodeSort Class for {}".format(self.filepath)

    def sort(self):
        """ Sorts the python file according to the sorting schema """
#
#        The Algorithm:
#        First, we obviously need to open the file.
#        Then we collect information on the classes, functions, global
#        variables, etc.
#        Each code block should be put into some kind of container
#        This container should have an attribute for the code block name
#        so that I can use that for sorting.
#        After parsing all code blocks into the container, sort them and
#        re-write them into a new file. Always into a new file. Overwriting
#        the old file would be a 2nd step.
#        If the user wants a new file created, then we're done.
#        If the user wants the original file overwritten (default), then
#        we open original file, delete all contents, and then copy all
#        contents from the new file into the original. I intentionally do not
#        want to just delete the original and rename the new because that
#        could mess up some SVN to backup functions (because the file
#        creation date would change, or perhaps there's a file UID that would
#        change).
        pass


class CodeBlock(object):
    """
    Class that contains info of a given code block. A code block will be
    from the decorator (if any) to the end of the indent.


    Public Methods:
        ???
        I can't think of any right now...

    Private Methods:
        count the number of lines
        set the type
        set the name
        run the init
    """

    def __init__(self, code_text):
        """ Init class attributes """
        self.code_text = code_text
        self.code_type = ''
        self.line_count = 0
        self.decorator_count = 0
        self.name = ""
        self._init_attributes()

    def __str__(self):
        """ String representation """
        str_rep = "A {block_type} named {name} with {num} lines."
        return str_rep.format(block_type=self.code_type,
                              name=self.name,
                              num=self.line_count,
                              )

    def _set_line_count(self):
        """ Private method that actually sets the line_count attribute """
        self.line_count = len(self.code_text.splitlines())

    def _set_type(self):
        """ Private methon that actually sets the type attribute """
        # Simple case: first line starts with 'class' or 'def'
        # first, move through any whitespace to get to the line starter
        # Remember, we don't actually want to change any of the original text.
        type_str = self.code_text.lstrip().split(' ')[0]
        if type_str == 'class':
            code_type = 'class'
        elif type_str == 'def':
            code_type = 'function'
        else:
            code_type = 'other'
        self.code_type = code_type

    def _set_name(self):
        """ Private methon that actually sets the name of the code block """
        # Simple naming, where the line is a func or class
        name = self.code_text.lstrip().split(' ')[1].split('(')[0]
        self.name = name

    def _set_decorator_count(self):
        """ Counts the number of decorators """
        # TODO: add decorator counting algorithm.
        count = 0
        self.decorator_count = count

    def _init_attributes(self):
        """ Runs all the various parsers """
        self._set_line_count()
        self._set_type()
        self._set_name()
        self._set_decorator_count()


def file_prompt():
    """ Prompt the user for the file path """
    exit_set = {'exit', 'e', 'quit', 'q'}
    print("Please enter a file to convert or parse:")
    while True:
        try:
            filepath = raw_input("File: ")
            if filepath.lower() in exit_set:
                filepath = 'exit'
                break
            elif os.path.isfile(filepath):
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid file. Please enter the path again.")
    return filepath


def classify_block(code_block):
    """ Classifies a code block to one a BLOCK_TYPE category """
    code_type = 'none'
    # First, we ignore any whitespace in front
    temp = code_block.lstrip()
    # if the line starts with an @ symbol, it's decorated, so we
    # need to look at the next line for the type. Repeat until a
    # type is found. It's also safe to assume it's a mulitline thing.
    if temp.startswith('@'):
        multiline = temp.splitlines()
        for line in multiline:
            if not line.startswith('@'):
                # apply the typing logic
                code_type = 'decorator'
                break
    elif temp.startswith('class'):
        # then it's a class, duh
        code_type = 'class'
    elif temp.startswith('def'):
        # a function or a method
        code_type = 'function'
    elif temp.startswith('#'):
        # a comment
        code_type = 'comment'
    elif temp.startswith('from') or temp.startswith('import'):
        # import statement
        code_type = 'import'
    elif temp.startswith('"""'):
        code_type = 'docstring'
    elif set(temp.split(' ')[0]) <= set(string.ascii_uppercase):
        code_type = 'constant'
    else:
        code_type = 'other'
    return code_type


def binary_file_compare(file1, file2):
    """
    Compares two files byte-by-byte. Usefull if the md5sum is different
    for some reason.
    """
    match = False
    with open(file1, 'rb') as ref:
        with open(file2, 'rb') as tmp:
            # File Size Check
            ref.seek(-1, 2)
            tmp.seek(-1, 2)
            ref_size = ref.tell()
            if not ref_size == tmp.tell():
                return match
            # Last byte check
            if not ref.read() == tmp.read():
                return match
            # move back to the begining and iterate through the file
            ref.seek(0, 0)
            tmp.seek(0, 0)
            for ref_byte, tmp_byte in zip(ref, tmp):
                match = ref_byte == tmp_byte
                if not match:
                    break
    return match


def main():
    """ Main Code """
    args = docopt(__doc__, version='v0.1')

    if args['FILE'] is None:
        args['FILE'] = file_prompt()
        if args['FILE'] == 'exit':
            print("Exiting Program")
            return

    if args['--new-file']:
        print("A new file will be made.")

# ---------------------------------------------------------
# Quick Testing
# ---------------------------------------------------------

    cs = CodeSort(args['FILE'])
    print(cs)

    block_1 = """class HelloKitty(object):
    def __init__(self):
        pass

    def method(self):
        return 5"""

    block_2 = """def my_function(a, b):
        return a + b"""

    # (block, (name, type, num_lines))
    known_values = ((block_1, ("HelloKitty", 'class', 6)),
                    (block_2, ("my_function", 'function', 2)),
                    )

    """ KVT for the CodeBlock class. """
    for block, expected in known_values:
        result_obj = CodeBlock(block)
        print(result_obj)

# ---------------------------------------------------------
# End Quick Testing
# ---------------------------------------------------------


if __name__ == "__main__":
    main()
