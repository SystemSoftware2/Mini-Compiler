'''
virtual machine for this compiler,
type of vm: stack virtual machine.
Usage:

vm = VirtualMachine()
vm.run([2, 5, 1, 'a', 2, 5, 1, 'b'])
Output:
Execution finished
a: 5
b: 5
'''

#Opcodes for VM
FETCH, STORE, PUSH, POP, ADD, SUB, MUL, DIV, LT, GT, EQ, NOTEQ, JZ, JNZ, JMP, PASS, HALT = range(17)

#Class for virtual machine
class VirtualMachine:
    def __init__(self):
        pass
    
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
