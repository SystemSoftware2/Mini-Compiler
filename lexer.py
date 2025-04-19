'''
lexer for this compiler.
Usage:

lexer = Lexer()
lexer.lex('a = 3')
print(lexer.sum)
('assign', 'a', '3')
'''

#Class for lexer
class Lexer:
    def __init__(self):
        pass

    def lex_term(self, value):
        '''
        finds the data type (int or id) of a
        value using regular expressions
        :value (str): values ​​to find the data type
        '''
        if re.match(r'[a-zA-Z][a-zA-Z0-9_]*', term):
            return ('id', term)
        elif re.match(r'[0-9]+', term):
            return ('num', term)

    def lex_expr(self, exp):
        '''
        two lex_term at indexes 0, 2 and an operation at index 1
        :exp (str): space-separated expression
        '''
        res = exp.split(' ')
        if len(res) == 1:
            return (self.lexterm(res[0]), res[0])
        first = self.lexterm(res[0])
        second = self.lexterm(res[2])
        return [first, res[1], second]
    
    def lex(self, string):
        '''
        function of lexing.
        self.sum: result of lexer
        string (str): string (not "a = 5; b = 5" but "a = 5")
        '''
        self.sum = None
        
        d = string.split(' ')
        #while loop
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
        #if
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
        #empty (pass)
        elif d[0] == 'empty':
            self.sum = ("empty", None)
            return None
        #else
        elif d[0] == 'else':
            stmt = string.replace('else ', '')
            if stmt == '':
                raise SyntaxError('Invalid "else" statement')
            self.sum = ("else", stmt)
            return None
        #exit (this is sys.exit(0) in python)
        elif d[0] == 'exit':
            self.sum = ('exit', None)
            return None
        try:
            #assign. example: a = 3
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
        #syntax error, if user entered incorrectly
        raise SyntaxError('Invalid syntax: '+str(string))
