"""

This file contains the language's values.

Classes:
  - Number - A Number value

"""

class Number:
 def __init__(self, value):
  self.value = value
  self.set_pos()
  self.set_context()

 def __repr__(self):
  return str(self.value)

 def set_context(self, context=None):
  self.context = None
  return self

 def set_pos(self, pos_start=None, pos_end=None):
  self.pos_start = None
  self.pos_end = None
  return self

 def added_to(self, other):
  if isinstance(other, Number):
   return Number(self.value + other.value).set_context(self.context), None

 def subbed_by(self, other):
  if isinstance(other, Number):
   return Number(self.value - other.value).set_context(self.context), None

 def multed_by(self, other):
  if isinstance(other, Number):
   return Number(self.value * other.value).set_context(self.context), None

 def dived_by(self, other):
  if isinstance(other, Number):
   try:
    num = Number(self.value / other.value).set_context(self.context)
    if str(num.value).endswith(".0"):
     num.value = int(str(num.value)[:-2])
    return num, None
   except ZeroDivisionError:
    return Number(0).set_context(self.context), None

 def powed_by(self, other):
  if isinstance(other, Number):
   return Number(self.value ** other.value).set_context(self.context), None