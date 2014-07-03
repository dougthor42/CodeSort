# -*- coding: utf-8 -*-
"""
Docstring!
"""


from __future__ import print_function, division


def ClassA(object):
    """ ClassA, for sorting! """
    def __init__(self,
                 var1,
                 var2):
        """ Single Line """
        pass

    def _private_a(self,
                   var1,
                   var2,
                   var3,
                   ):
        """ Multiline, standard indent level """
        pass

    def _private_b(self,
var1,
var2,
var3,
):
        """ Multiline, no indent """
        pass

    def _private_c(self,
           var1,
       var2,
               var3,
         ):
        """ multiline, weird indent """
        pass
