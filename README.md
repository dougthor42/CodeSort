codesort
========
A Python source-code organization tool.

The goal of this project is to create a tool that will take a python source code file (.py) and organize it to some standard by moving around class and function defintions, while still maintaining original functionality.

The organization will be as follows:

    1. source file encoding (the "# -*- coding: utf-8 -*-" at the start of the file)
    
    2. module docstring
    
    3. __future__ import statements
    
    4. import statements
    
    5. module constants
    
    6. classes
    
    7. module functions
    
    8. main() function
    
    9. toplevel module code
    
    10. if __name__ == '__main__': block


Classes are to be organized in the following way:

class docstring
    __init__
    
    __new__
    
    __del__
    
    __str__
    
    __repr__
    
    __cmp__
    
    __hash__
    
    __nonzero__
    
    __unicode__
    
    __getattr__
    
    __setattr__
    
    __delattr__
    
    __getattribute__
    
    __get__
    
    __set__
    
    __delete__
    
    <private methods>
    
    <public methods>


the private methods are organized alphabetically
the public methods are organized alhpabetically


module functions are organized alphabetically, except for the main() function, which is always at the end of the module functions
