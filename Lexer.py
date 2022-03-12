"""

This file contains the language's Lexer.

Classes:
  - Lexer - The main Lexer class

"""

from Token import *
from Position import *
from Constants import *

# Import all Classes from the classes directory
from pathlib import Path
for classfile in Path.cwd().joinpath('classes').iterdir():
 file = classfile.name
 if file.endswith('.py'):
  exec('from classes.'+file[:-3]+' import *')

class Lexer:
 def __init__(self, fn, text):
  self.fn = fn
  self.text = text
  self.pos = Position(-1, 0, -1, fn, text)
  self.current_char = None
  self.advance()

 def advance(self):
  self.pos.advance(self.current_char)
  self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
 
 def make_tokens(self):
  tokens = []

  while self.current_char != None:
   if self.current_char in ALPHABET:
    tokens.append(Token('LETTER', pos_start=self.pos, value=self.current_char))
    self.advance()
   elif self.current_char in DIGITS:
    tokens.append(self.make_number())
    self.advance()
   elif self.current_char == '+':
    tokens.append(Token('PLUS', pos_start=self.pos))
    self.advance()
   elif self.current_char == '-':
    tokens.append(Token('MINUS', pos_start=self.pos))
    self.advance()
   elif self.current_char == '*':
    tokens.append(Token('MUL', pos_start=self.pos))
    self.advance()
   elif self.current_char == '/':
    tokens.append(Token('DIV', pos_start=self.pos))
    self.advance()
   elif self.current_char == '(':
    tokens.append(Token('LPAREN', pos_start=self.pos))
    self.advance()
   elif self.current_char == ')':
    tokens.append(Token('RPAREN', pos_start=self.pos))
    self.advance()
   elif self.current_char == ' ':
    self.advance()
   else:
    pos_start = self.pos.copy()
    char = self.current_char
    self.advance()
    return [], IllegalCharError(pos_start, self.pos, char)

  tokens.append(Token('EOF', pos_start=self.pos))
  return tokens, None

 def make_number(self):
  num_str = ''
  dot_count = 0
  pos_start = self.pos.copy()

  while self.current_char != None and self.current_char in DIGITS + '.':
   if self.current_char == '.':
    if dot_count == 1: break
    dot_count += 1
    num_str += '.'
   else:
    num_str += self.current_char
   self.advance()

  if dot_count == 0:
   return Token('INT', int(num_str), pos_start, self.pos)
  else:
   return Token('FLOAT', float(num_str), pos_start, self.pos)
