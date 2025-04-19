'''
parser for this compiler.
Usage:

parser = Parser()
for i in parser.parse('a = 3; while (a < 5) a = a + 1')):
  print(i)
Output:
Node(name='ASSIGN', op1=a, op2=Node(name='INT', 3), op3=None)
Node(name='WHILE', op1=Node(name='<', op1=Node(name='ID', op1=a), op2=Node(name='INT', op1=5)), op2=Node(name='ASSIGN', op1=a, op2=Node(name='+', op1=Node(name='ID', op1=a), op2=Node(name='INT', op1=1))))
'''

try:
    from .lexer import *
except:
    from lexer import *

#Class for AST Node
class Node:
    def __init__(self, name, op1, op2=None, op3=None):
        self.name = name
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self):
        return f"Node(name='{self.name}', op1={self.op1}, op2={self.op2}, op3={self.op3})"

    __str__ = __repr__

#Class for parser
class Parser:
    def __init__(self, lexer):
        self.pos = 0
        self.lexer = lexer

    def term(self, value):
        if value[0] == 'id':
            return 'ID'
        elif value[0] == 'num':
            return 'INT'

    def parse_expr(self, token):
        try:
            left = token[0]
            right = token[2]
            op = token[1]

            result = Node(op, Node(self.term(left), left[1]), Node(self.term(right), right[1]))
            return result
        except:
            try:
                return Node(self.term(left), left[1])
            except:
                raise SyntaxError('Invalid expression')

    def paren_expr(self, expr):
        d = expr[expr.index('(') + 1:expr.index(')')]
        return self.parse_expr(self.lexer.lex_expr(d))

    def parse(self, program):
        try:
            self.prog = program.split('; ')
        except:
            self.prog = program
        astpos = 0
        ast = []
        while self.pos < len(self.prog):
            if self.prog[self.pos] == '':
                self.pos += 1
                continue
            d = self.prog[len(self.prog) - 1]
            r = len(d) - 1
            if d[r] == ';':
                raise SyntaxError('The ";" sign is not needed at the end')
            self.lexer.next_token(self.prog[self.pos])
            token = self.lexer.sum
            if token[0] == 'assign':
                ast.append(Node('ASSIGN', token[1], op2=self.parse_expr(self.lexer.lex_expr(token[2]))))
            elif token[0] == 'if':
                d = Lexer()
                r = Parser(d)
                ast.append(Node('IF', self.paren_expr(token[1]), op2=r.parse(token[2])[0]))
            elif token[0] == 'while':
                d = Lexer()
                r = Parser(d)
                ast.append(Node('WHILE', self.paren_expr(token[1]), op2=r.parse(token[2])[0]))
            elif token[0] == 'else':
                d = Lexer()
                r = Parser(d)
                if ast[astpos - 1].name == 'IF':
                    ast[astpos - 1].name = 'ELSE'
                    ast[astpos - 1].op3 = r.parse(token[1])[0]
                else:
                    raise SyntaxError('Invalid "else" statement')
            elif token[0] == 'exit':
                ast.append(Node('EXIT', None))
            elif token[0] == 'pass':
                ast.append(Node('PASS', None))
            self.pos += 1
            astpos += 1
        return ast
