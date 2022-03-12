"""

This file contains the language's Interpreter.

Classes:
  - Interpreter - The main Interpreter class
  - RTResult    - Runtime Result class

"""

from classes.Error import *
from Values import *
from Token import *
from Nodes import *

class RTResult:
 def __init__(self):
  self.value = None
  self.error = None

 def register(self, res):
  if res.error: self.error = res.error
  return res.value

 def success(self, value):
  self.value = value
  return self

 def failure(self, value):
  self.error = error
  return self

class Interpreter:
 def visit(self, node):
  method_name = f'visit_{type(node).__name__}'
  method = getattr(self, method_name, self.no_visit_method)
  return method(node)

 def no_visit_method(self, node):
  raise InternalError(f'No visit method for {type(node).__name__} found.')

 def visit_NumberNode(self, node):
  return RTResult().success(Number(node.tok.value).set_pos(node.pos_start, node.pos_end))

 def visit_BinOpNode(self, node):
  res = RTResult()
  left = res.register(self.visit(node.left_node))
  if res.error: return res
  right = res.register(self.visit(node.right_node))
  if res.error: return res

  if node.op_tok.type == PLUS:    result, error = left.added_to(right)
  elif node.op_tok.type == MINUS: result, error = left.subbed_by(right)
  elif node.op_tok.type == MUL:   result, error = left.multed_by(right)
  elif node.op_tok.type == DIV:   result, error = left.dived_by(right)

  if error: return res.failure(error)
  else: return res.success(result.set_pos(node.pos_start, node.pos_end))

 def visit_UnaryOpNode(self, node):
  res = RTResult()
  number = res.register(self.visit(node.node))
  if res.error: return res

  error = None

  if node.op_tok.type == MINUS: number, error = number.multed_by(Number(-1))

  if error: return res.failure(error)
  else: return res.success(number.set_pos(node.pos_start, node.pos_end))