# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 17:06:51 2014

@name:          new_program.py
@vers:          0.1
@author:        dthor
@created:       Wed Jul 02 17:06:51 2014
@modified:      Wed Jul 02 17:06:51 2014
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function
from docopt import docopt
import codesort.ffp2 as ffp


def main():
    """ Main Code """
    docopt(__doc__, version='v0.1')


if __name__ == "__main__":
#    main()
    pass
