#codesort
A Python source-code organization tool.

The goal of this project is to create a tool that will take a python source code file (.py) and organize it to some standard by moving around class and function defintions, while still maintaining original functionality.

###The organization will be as follows:

>1. source file encoding (the "# -*- coding: utf-8 -*-" at the start of the file)
>2. module docstring
>3. \__future__ import statements
>4. import statements
>5. module constants
>6. classes
>7. module functions
>8. main() function
>9. toplevel module code
>10. if \__name__ == '\__main__' block


###Classes are to be organized in the following way:

>0. class docstring
>1. \__init__
>2. \__new__
>3. \__del__
>4. \__str__
>5. \__repr__
>6. \__cmp__
>7. \__hash__
>8. \__nonzero__
>9. \__unicode__
>10. \__getattr__
>11. \__setattr__
>12. \__delattr__
>13. \__getattribute__
>14. \__get__
>15. \__set__
>16. \__delete__
>17. \<private methods>
>18. \<public methods>


Private and private methods are organized alphabetically.

Module functions are organized alphabetically, except for the main() function, which is always at the end of the module functions
