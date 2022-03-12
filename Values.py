"""

This file contains the language's values.

Classes:
  - Number - A Number value

"""

class Number:
 def __init__(self, value):
  self.value = value
  self.set_pos()

 def __repr__(self):
  return str(self.value)

 def set_pos(self, pos_start=None, pos_end=None):
  self.pos_start = None
  self.pos_end = None
  return self

 def added_to(self, other):
  if isinstance(other, Number):
   return Number(self.value + other.value), None

 def subbed_by(self, other):
  if isinstance(other, Number):
   return Number(self.value - other.value), None

 def multed_by(self, other):
  if isinstance(other, Number):
   return Number(self.value * other.value), None

 def dived_by(self, other):
  if isinstance(other, Number):
   try:
    return Number(self.value / other.value), None
   except ZeroDivisionError:
    return Number(0), None