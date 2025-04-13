import re
import sys

BNF = '''
<program> ::= <statement>
<statement> ::= <while> | <if> | <assign>
<while> ::= "while " <paren_expr> " " <statement>
<if> ::= "if " <paren_expr> " " <statement> | "if " <paren_expr> " " <statement> " else " <statement>
<paren_expr> ::= "(" <exp> ")"
<assign> ::= <indent> " = " <exp> "; " | <indent> " = " <exp>
<indent> ::= [a-z] | [A-Z]
<digit> ::= [0-9]
<exp> ::= <term> | <bexp> | <aexp>
<term> ::= <digit> | <indent>
<bexp> ::= <term> " > " <term> | <term> " < " <term> | <term> " == " <term> | <term> " != " <term>
<aexp> ::= <term> " + " <term> | <term> " - " <term> | <term> " * " <term> | <term> " / " <term>
'''
FETCH, STORE, PUSH, POP, ADD, SUB, MUL, DIV, LT, GT, EQ, NOTEQ, JZ, JNZ, JMP, PASS, HALT = range(17)

class Lexer:
    def __init__(self):
        pass

    def lexterm(self, term):
        if re.match(r'[a-zA-Z][a-zA-Z0-9_]*', term):
            return ('id', term)
        elif re.match(r'[0-9]+', term):
            return ('num', term)

    def lex_expr(self, exp):
        res = exp.split(' ')
        if len(res) == 1:
            return (self.lexterm(res[0]), res[0])
        first = self.lexterm(res[0])
        second = self.lexterm(res[2])
        return [first, res[1], second]
    
    def next_token(self, string):
        self.sum = None
        
        d = string.split(' ')
        if d[0] == 'while':
            d = string.split(')')
            try:
                cond = d[0][d[0].index('while') + 6:] + ')'
            except:
                raise SyntaxError('Invalid paren expression')
            try:
                stmt = d[1][1:]
            except:
                raise SyntaxError('Invalid "while" statement')
            self.sum = ("while", cond, stmt)
            return None
        elif d[0] == 'if':
            d = string.split(')')
            try:
                cond = d[0][d[0].index('if') + 3:] + ')'
            except:
                raise SyntaxError('Invalid paren expression')
            try:
                stmt = d[1][1:]
            except:
                raise SyntaxError('Invalid "if" statement')
            self.sum = ("if", cond, stmt)
            return None
        elif d[0] == 'pass':
            self.sum = ("pass", None)
            return None
        elif d[0] == 'else':
            stmt = string.replace('else ', '')
            if stmt == '':
                raise SyntaxError('Invalid "else" statement')
            self.sum = ("else", stmt)
            return None
        elif d[0] == 'exit':
            self.sum = ('exit', None)
            return None
        try:
            if d[1] == '=':
                name = d[0]
                valu = d[2:]
                pos = 0
                value = ''
                while pos < len(valu):
                    if pos + 1 == len(valu):
                        value += valu[pos]
                    else:
                        value += valu[pos] + ' '
                    pos += 1
                self.sum = ("assign", name, value)
                return None
        except:
            pass
        raise SyntaxError('Invalid syntax: '+str(string))

class Node:
    def __init__(self, name, op1, op2=None, op3=None):
        self.name = name
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self):
        return f"Node(\n  name='{self.name}',\n  op1={self.op1},\n  op2={self.op2},\n  op3={self.op3}\n)"

    __str__ = __repr__

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

class Compiler:
    def __init__(self):
        self.program = []
        self.pc = 0

    def gen(self, command):
        self.program.append(command)
        self.pc = self.pc + 1

    def compilenode(self, node):
        name = node.name
        if name == 'INT':
            self.gen(PUSH)
            self.gen(int(node.op1))
        elif name == 'ID':
            self.gen(FETCH)
            self.gen(node.op1)
        elif name == '+':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(ADD)
        elif name == '-':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(SUB)
        elif name == '/':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(DIV)
        elif name == '*':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(MUL)
        elif name == '<':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(LT)
        elif name == '>':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(GT)
        elif name == '!=':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(NOTEQ)
        elif name == '==':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(EQ)
        elif name == 'ASSIGN':
            self.compilenode(node.op2)
            self.gen(STORE)
            self.gen(node.op1)
        elif name == 'IF':
            self.compilenode(node.op1)
            self.gen(JZ)
            addr = self.pc
            self.gen(0)
            self.compilenode(node.op2)
            self.program[addr] = self.pc
        elif name == 'ELSE':
            self.compilenode(node.op1)
            self.gen(JZ)
            addr1 = self.pc
            self.gen(0)
            self.compilenode(node.op2)
            self.gen(JMP)
            addr2 = self.pc
            self.gen(0)
            self.program[addr1] = self.pc
            self.compilenode(node.op3)
            self.program[addr2] = self.pc
        elif name == 'WHILE':
            if node.op1.op2:
                try:
                    r = node.op1.op2
                    d = str(int(r.op1) - 1)
                    r.op1 = d
                except:
                    r = node.op1.op1
                    d = str(int(r.op1) - 1)
                    r.op1 = d
            addr1 = self.pc
            self.compilenode(node.op1)
            self.gen(JZ)
            addr2 = self.pc
            self.gen(1)
            self.compilenode(node.op2)
            self.gen(JMP)
            self.gen(addr1)
            self.program[addr2] = self.pc
        elif name == 'EXIT':
            self.gen(HALT)
        elif name == 'PASS':
            self.gen(PASS)
                    
    def compileast(self, ast):
        for i in ast:
            self.compilenode(i)
        self.gen(HALT)
        return self.program

class VirtualMachine:
    def run(self, program):
        env = {}
        stack = []
        pc = 0
        while True:
            op = program[pc]
            if pc < len(program) - 1:
                arg = program[pc + 1]

            if op == FETCH:
                try:
                    stack.append(env[arg])
                except:
                    stack.append(0)
                pc += 2
            elif op == STORE:
                env[arg] = stack.pop()
                pc += 2
            elif op == PUSH:
                stack.append(arg)
                pc += 2
            elif op == ADD:
                stack[-2] += stack[-1]
                stack.pop()
                pc += 1
            elif op == SUB:
                stack[-2] -= stack[-1]
                stack.pop()
                pc += 1
            elif op == MUL:
                stack[-2] *= stack[-1]
                stack.pop()
                pc += 1
            elif op == DIV:
                stack[-2] /= stack[-1]
                stack.pop()
                pc += 1
            elif op == LT:
                if stack[-2] <= stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == GT:
                if stack[-2] >= stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == EQ:
                if stack[-2] == stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == NOTEQ:
                if stack[-2] != stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == POP:
                stack.append(arg)
                stack.pop()
                pc += 1
            elif op == JZ:
                    if stack.pop() == 0:
                          pc = arg
                    else:
                        pc += 2
            elif op == JNZ: 
                    if stack.pop() != 0:
                          pc = arg
                    else:
                          pc += 2
            elif op == JMP:
                pc = arg
            elif op == PASS:
                pc += 1
            elif op == HALT:
                break

        print('Execution finished')
        for i in env.keys():
            print(i+': '+str(env[i]))

def run_compiler(prog):
    lexer = Lexer()
    parser = Parser(lexer)
    ast = parser.parse(prog)

    compiler = Compiler()
    bytecode = compiler.compileast(ast)

    vm = VirtualMachine()
    vm.run(bytecode)

def cli():
    while True:
        com = input('>>> ')
        else:
            try:
                run_compiler(com)
            except Exception as err:
                print('Error: ', end="")
                sys.stderr.write(str(err)+'\n')

if __name__ == '__main__':
    cli()
