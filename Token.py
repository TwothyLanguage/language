"""

This file contains all token types and handling.

Classes:
  - Token - The main Token class

"""

from Position import *

INT    = 'INT'
FLOAT  = 'FLOAT'
PLUS   = 'PLUS'
MINUS  = 'MINUS'
MUL    = 'MULTIPLY'
DIV    = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LETTER = 'LETTER'
EOF    = 'EOF'

class Token:
 def __init__(self, type_, value=None, pos_start=Position(0, 0, 0, 0, "Unknown"), pos_end=Position(0, 0, 0, 0, "Unknown")):
  self.type = eval(type_)
  self.value = value

  if pos_start:
   self.pos_start = pos_start.copy()
   self.pos_end = pos_start.copy()
   self.pos_end.advance()
  if pos_end:
   self.pos_end = pos_end.copy()

 def __repr__(self):
  if self.value: return f'{self.type}:{self.value}'
  return f'{self.type}'
