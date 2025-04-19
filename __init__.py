'''
For run code on this compiler.
Example:
from compiler import *

run_compiler('a = 3; while (a < 5) a = a + 1')
Output:
Execution finished
a: 5
'''
from .compiler import *
from .parser import *
from .lexer import *
from .vm import *
import sys

def run_code(code):
  lexer = Lexer()
  parser = Parser(lexer)
  
  ast = parser.parse(code)
  
  VirtualMachine().run(Compiler().compileast(ast))

def cli():
  while True:
    com = input('>>> ')
    if com == 'quit':
      break
    try:
      run_code(com)
    except Exception as err:
      print('Error:', end=" ")
      sys.stderr.write(str(err)+'\n')
