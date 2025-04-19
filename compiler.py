'''
compiler.
Usage:

from parser import Node

compiler = Compiler()
print(compiler.compileast([Node('ASSIGN', 'a', op2=Node('INT', '5'))])
Output:
[2, 5, 1, 16]
'''

FETCH, STORE, PUSH, POP, ADD, SUB, MUL, DIV, LT, GT, EQ, NOTEQ, JZ, JNZ, JMP, PASS, HALT = range(17)

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
                    if node.op1.name == '<':
                        d = str(int(r.op1) - 1)
                    else:
                        d = str(int(r.op1))
                    r.op1 = d
                except:
                    r = node.op1.op1
                    if node.op1.name == '<':
                        d = str(int(r.op1) - 1)
                    else:
                        d = str(int(r.op1))
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
