import re
from interpreter import Num,Str,Var,Assign,Print,BinOp

token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),
    ('STRING',   r'"[^"]*"'),
    ('ID',       r'[A-Za-z_]\w*'),
    ('ASSIGN',   r'='),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MUL',      r'\*'),
    ('DIV',      r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('SEMICOLON',r';'),
    ('COMMA',    r','),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
]

def tokenize(code):
    tok_regex = '|'.join('(?P<%s>%s)' % (n,p) for n,p in token_specification)
    get_token = re.compile(tok_regex).match
    pos=0
    mo=get_token(code,pos)
    tokens=[]
    while mo:
        kind=mo.lastgroup
        value=mo.group()
        if kind not in ('SKIP','NEWLINE'):
            tokens.append((kind,value))
        pos=mo.end()
        mo=get_token(code,pos)
    return tokens

class Parser:
    def __init__(self,tokens):
        self.tokens=self.tokens=tokens
        self.pos=0
    def peek(self):
        return self.tokens[self.pos] if self.pos<len(self.tokens) else None
    def eat(self,kind):
        token=self.peek()
        if not token or token[0]!=kind: raise SyntaxError("Expected %s, got %s"%(kind,token))
        self.pos+=1
        return token
    def parse_stmt(self):
        token=self.peek()
        if token[0]=='ID':
            name=self.eat('ID')[1]
            self.eat('ASSIGN')
            expr=self.parse_expr()
            self.eat('SEMICOLON')
            return Assign(name,expr)
        if token[0]=='ID' and token[1]=='show':
            self.eat('ID'); self.eat('LPAREN')
            expr=self.parse_expr()
            self.eat('RPAREN'); self.eat('SEMICOLON')
            return Print(expr)
    def parse_expr(self):
        token=self.peek()
        if token[0]=='NUMBER': self.eat('NUMBER'); return Num(float(token[1]))
        if token[0]=='STRING': self.eat('STRING'); return Str(token[1][1:-1])
