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

 def failure(self, error):
  self.error = error
  return self

class Interpreter:
 def visit(self, node, context):
  method_name = f'visit_{type(node).__name__}'
  method = getattr(self, method_name, self.no_visit_method)
  return method(node, context)

 def no_visit_method(self, node, context):
  err = InternalError()
  err.STACKTRACE = [f'An internal error occured; No visit method for {type(node).__name__} found.']
  return RTResult().failure(err.throw())

 def visit_VarAccessNode(self, node, context):
  res = RTResult()
  var_name = node.var_name_tok.value
  value = context.symbol_table.get(var_name)

  if not value: return res.failure(RTError(POS_START=node.pos_start,details=f'\'{var_name}\' is not defined', CONTEXT=context))
  return res.success(value)

 def visit_VarAssignNode(self, node, context):
  res = RTResult()
  var_name = node.var_name_tok.value
  value = res.register(self.visit(node.value_node, context))
  if res.error: return res

  context.symbol_table.set(var_name, value)
  return res.success(value)

 def visit_NumberNode(self, node, context):
  return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

 def visit_BinOpNode(self, node, context):
  res = RTResult()
  left = res.register(self.visit(node.left_node, context))
  if res.error: return res
  right = res.register(self.visit(node.right_node, context))
  if res.error: return res

  if node.op_tok.type == PLUS:    result, error = left.added_to(right)
  elif node.op_tok.type == MINUS: result, error = left.subbed_by(right)
  elif node.op_tok.type == MUL:   result, error = left.multed_by(right)
  elif node.op_tok.type == DIV:   result, error = left.dived_by(right)
  elif node.op_tok.type == POW:   result, error = left.powed_by(right)

  if error: return res.failure(error)
  else: return res.success(result.set_pos(node.pos_start, node.pos_end))

 def visit_UnaryOpNode(self, node, context):
  res = RTResult()
  number = res.register(self.visit(node.node, context))
  if res.error: return res

  error = None

  if node.op_tok.type == MINUS: number, error = number.multed_by(Number(-1))

  if error: return res.failure(error)
  else: return res.success(number.set_pos(node.pos_start, node.pos_end))