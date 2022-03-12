"""

This file contains all general Error-related classes which run off the main "Error" class.
The error classes which are based off of the main Error class will have functions to get it
as a plain Error classs.

Classes:
  - Error              - The main Error class
  - IllegalCharError   - The Error class for illegal characters
  - InvalidSyntaxError - The Error class for invalid syntax

"""
class Error:
 """
 
 The main Error class for Twothy. 

 Fields:
   - PRINT_ONLY:        Boolean - Whether to only print the text and not stop the code until further input.
   - ERROR_TEXT:        String  - The text to display in the error.
   - STACKTRACE:        List
     - #1 (Position):   String


 Methods:
   - __init__():        None    - Takes all fields as an optional variable to create a new error to call.
   - printStacktrace(): None    - Prints the error stacktrace.
   - throw():           None    - Throws an error and if PRINT_ONLY is false raises python's SystemExit exception.

 """

 PRINT_ONLY = True
 ERROR_TEXT = "An unexpected error occured."
 STACKTRACE = ["Unknown"]

 # Returns: None
 def __init__(self, START_POS=None, END_POS=None, PRINT_ONLY=PRINT_ONLY,ERROR_TEXT=ERROR_TEXT,STACKTRACE=STACKTRACE):
  self.START_POS  = START_POS
  self.END_POS    = END_POS
  self.PRINT_ONLY = PRINT_ONLY
  self.ERROR_TEXT = ERROR_TEXT
  self.STACKTRACE = STACKTRACE
  return None

 # Returns: None
 def printStacktrace(self):
  f = "Stacktrace: "
  for stline in self.STACKTRACE:
   f = f + stline + "\n"
  print(f)
  return None

 # Returns: None
 def throw(self):
  print(self.ERROR_TEXT)
  self.printStacktrace()
  if not self.PRINT_ONLY:
   input("")
   raise SystemExit
  return None

class IllegalCharError(Error):
 """
 
 The Error class for illegal characters. Inherits fields and methods from Error class.

 Methods:
   - get(): Error - Returns the IllegalCharError as an Error

 """
 def __init__(self, START_POS, END_POS, illegalChar):
  super().__init__(START_POS, END_POS, ERROR_TEXT='Illegal Character',STACKTRACE=[f'Illegal character; {str(illegalChar)}', f'File {START_POS.fn}, line {START_POS.ln + 1}'])

 def get(self):
  return Error(self.PRINT_ONLY, self.ERROR_TEXT, self.STACKTRACE)

class InvalidSyntaxError(Error):
 """
 
 The Error class for invalid syntax. Inherits fields and methods from Error class.

 Methods:
   - get(): Error - Returns the InvalidSyntaxError as an Error

 """
 def __init__(self, START_POS, END_POS, invalidSyntax=''):
  super().__init__(START_POS, END_POS, ERROR_TEXT='Invalid Syntax',STACKTRACE=[f'{invalidSyntax}', f'File {START_POS.fn}, line {START_POS.ln + 1}'])

 def get(self):
  return Error(self.PRINT_ONLY, self.ERROR_TEXT, self.STACKTRACE)

class InternalError(Error):
 """
 
 The Error class for internal errors. Inherits fields and methods from Error class.

 Methods:
   - get(): Error - Returns the InternalError as an Error

 """
 def __init__(self, extra=''):
  super().__init__(None, None, ERROR_TEXT='Internal Error',STACKTRACE=[f'An internal error occured; {extra}.'])

 def get(self):
  return Error(self.PRINT_ONLY, self.ERROR_TEXT, self.STACKTRACE)