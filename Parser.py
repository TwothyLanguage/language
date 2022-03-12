"""

This file contains the language's Parser.

Classes:
  - Parser      - The main Parser class
  - ParseResult - The Parser result class.

"""

from Token import *
from classes.Error import *
from Nodes import *

class ParseResult:
 def __init__(self):
  self.error = None
  self.node = None

 def register(self, res):
  if isinstance(res, ParseResult):
   if res.error: self.error = res.error
   return res.node

  return res

 def success(self, node):
  self.node = node
  return self

 def failure(self, error):
  self.error = error
  return self

class Parser:
 def __init__(self, tokens):
  self.tokens = tokens
  self.tok_idx = -1
  self.advance()

 def advance(self):
  self.tok_idx += 1
  if self.tok_idx < len(self.tokens):
   self.current_tok = self.tokens[self.tok_idx]
  return self.current_tok

 def parse(self):
  res = self.expr()
  if not res.error and self.current_tok.type != 'EOF':
   return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,"Expected '+', '-', '*', '/' or '%'"))
  return res

 def atom(self):
  res = ParseResult()
  tok = self.current_tok

  if tok.type in (INT, FLOAT):
   res.register(self.advance())
   return res.success(NumberNode(tok))

  elif tok.type == LPAREN:
   res.register(self.advance())
   expr = res.register(self.expr())
   if res.error: return res
   if self.current_tok.type == RPAREN:
    res.register(self.advance())
    return res.success(expr)
   else:
    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,"Expected ')'"))

 def power(self):
  return self.bin_op(self.atom, (POW, ), self.factor)
  
 def factor(self):
  res = ParseResult()
  tok = self.current_tok

  if tok.type in (PLUS, MINUS):
   res.register(self.advance())
   factor = res.register(self.factor())
   if res.error: return res
   return res.success(UnaryOpNode(tok, factor))

  return self.power()

 def term(self):
  return self.bin_op(self.factor, (MUL, DIV))

 def expr(self):
  return self.bin_op(self.term, (PLUS, MINUS))

 def bin_op(self, func_a, ops, func_b=None):
  if func_b == None:
   func_b = func_a
  res = ParseResult()
  left = res.register(func_a())
  if res.error: return res

  while self.current_tok.type in ops:
   op_tok = self.current_tok
   res.register(self.advance())
   right = res.register(func_b())
   if res.error: return res
   left = BinOpNode(left, op_tok, right)

  return res.success(left)