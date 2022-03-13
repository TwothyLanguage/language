"""

This file is the basic shell for the language.

"""

# Import everything in main directory
from pathlib import Path
for classfile in Path.cwd().iterdir():
 file = classfile.name
 if file.endswith('.py'):
  exec('from '+file[:-3]+' import *')

from classes.Error import *

global_symbol_table = SymbolTable()
global_symbol_table.set("True",  Number(1),            True)
global_symbol_table.set("False", Number(0),            True)
global_symbol_table.set("Pi",    Number(3.1415926535), True)

def run(fn, text):
 lexer = Lexer(fn, text)
 tokens, error = lexer.make_tokens()
 if error: return None, error

 parser = Parser(tokens)
 ast = parser.parse()
 if ast.error: return None, ast.error

 interpreter = Interpreter()
 context = Context('<program>')
 context.symbol_table = global_symbol_table
 result = interpreter.visit(ast.node, context)

 return result.value, result.error

while 1:
 text = input("twothy > ")
 result, error = run('<stdin>', text)

 if error: error.throw()
 else: print(result)