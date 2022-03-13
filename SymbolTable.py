"""

This file contains a symbol table class for holding variables

Classes:
  - SymbolTable - The main symbol table class

"""

from classes.Error import *

class SymbolTable:
 def __init__(self):
  self.symbols = {}
  self.protectedSymbols = {}
  self.parent = None

 def get(self, name):
  value = self.symbols.get(name, None)
  if value == None and self.parent:
   return self.parent.get(name)
  return value

 def getProtectedState(self, name):
  value = self.protectedSymbols.get(name, None)
  if value == None and self.parent:
   return False
  return value

 def set(self, name, value, protected=False):
  if self.getProtectedState(name):
   Error(PRINT_ONLY=True,STACKTRACE=[f'Unable to edit variable {name}: Variable is protected.']).throw()
  else:
   self.symbols[name] = value
   if protected:
    self.protectedSymbols[name] = value

 def remove(self, name):
  if self.getProtectedState(name):
   Error(PRINT_ONLY=True,STACKTRACE=[f'Unable to delete variable {name}: Variable is protected.']).throw()
  else:
   del self.symbols[name]