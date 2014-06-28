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
import re
import tokenize
import StringIO


__author__ = "Douglas Thor"


BLOCK_TYPE = [(re.compile(r'[ ]*@.'), 'decorator'),
              (re.compile(r'[ ]*class .'), 'class'),
              (re.compile(r'[ ]*def .'), 'function'),
              (re.compile(r'[ ]*#.'), 'comment'),
              (re.compile(r'[ ]*from .'), 'import'),
              (re.compile(r'[ ]*import .'), 'import'),
              (re.compile(r'[ ]*""".'), 'docstring'),
              (re.compile(r'[ ]*[A-Z0-9_]+ = .*'), 'constant'),
              (re.compile(r'[ ]*[a-z0-9_]+ = .*'), 'instance_var'),
              (re.compile(r'[ ]*.'), 'other'),
              ]


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


    Public Methods:BLOCK_TYPE
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
        self.code_type = classify_block(self.code_text)

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
    """ Classifies a code block to one BLOCK_TYPE category """
    match = False

    for regex_key, code_type in BLOCK_TYPE:
        if regex_key.match(code_block):
            # if it's a decorator, we need to go deeper
            if code_type == 'decorator':
                new_block = '\n'.join(code_block.split('\n')[1:])
                code_type = classify_block(new_block)
            return code_type

    if not match:
        return 'unknown'


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


def split_into_blocks(code_block):
    """ Splits code_block into it's compenents. Can be use recursively? """
    # In python, code blocks are separated by whitespace, so we need to find
    # those and use that as our delimiter. Keep in mind that there are things
    # that invalidate whitespace, such as (, ", """, ', ''', [, and {.

    block_starts = (
                    "def",
                    "class",
                    )

    use_file = 0
    if use_file == 1:
        temp = open(code_block)
        a = tokenize.generate_tokens(temp.readline)
        temp.close()

    else:
        a = tokenize.generate_tokens(StringIO.StringIO(code_block).readline)

    print(a)
    result = []
    indent_pos = 0
    in_block = False
    skip_to_newline = False
    log_str = "{num}\t{name}\t{indent}\t{st}\t{end}\t|{line}"
    for toknum, tokval, srowcol, erowcol, logical_l in a:
        print(log_str.format(num=toknum,
                             name=tokval.strip(),
                             st=srowcol,
                             end=erowcol,
                             line=logical_l.rstrip(),
                             indent=indent_pos,
                             ))

        if skip_to_newline:
            if not toknum == tokenize.NEWLINE:
                continue
            else:
                skip_to_newline = False
                continue
        # each time we see an indent token, we need to add 1 to a counter
        # the dedent subtracts one.
        # when the counter is 0, then we've ended our block.
        if toknum == tokenize.INDENT:
            indent_pos += 1
        if toknum == tokenize.DEDENT:
            indent_pos -= 1

        if toknum == tokenize.NAME and tokval in block_starts and not in_block:
            # then we start the block
            in_block = True
            start_row = srowcol[0]
            print("Start Row: {row}\t{name}".format(row=start_row,
                                                    name=tokval,
                                                    ))
            # we need some way to continue until the next logical line is found
            skip_to_newline = True
            continue

        if indent_pos == 0 and in_block:
            in_block = False
            # we want to consider the end line to be the line above, hence -1
            end_row = srowcol[0] - 1
            print("End Row: {row}".format(row=end_row))
            result.append((start_row, end_row))

    print(result)
    return result


    # If I use the tokenize values, then it appears that a block:
    #   1. Starts on the line abve the tokenize.INDENT (5) token
    #   2. Ends on the next tokenize.DEDENT (6) token.
    #   3. should only be counted as a major block if
    #       1. the first tokenize.NAME (1) token is def, class, etc.
    #       2. there is 1 or 2 tokenize.NL (54) tokens preceeding it
    # the number of dedents before the NAME token will tell you what level
    # you're on. Example: going in with 3 indents but then only 2 dedents
    # means you're still in the main block.

    # if a line starts with 4 spaces (or more) then it's a block. Let's
    # start with that.


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

    # KVT for the CodeBlock class.
    for block, expected in known_values:
        result_obj = CodeBlock(block)
        print(result_obj)

    print()
    print()
# ---------------------------------------------------------
# End Quick Testing
# ---------------------------------------------------------


if __name__ == "__main__":
    print("Random code addition for SVN check")
    main()
