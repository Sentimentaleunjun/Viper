import re
from interpreter import *

TOKEN_SPEC = [
    ("COMMENT", r"//.*"),                          # 한 줄 주석
    ("MCOMMENT", r"/\*[\s\S]*?\*/"),               # 여러 줄 주석
    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r'"[^"]*"'),
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OP", r"==|!=|<=|>=|&&|\|\||!|[+\-*/%<>=]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("COLON", r":"),
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\n"),
]

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        pos = 0
        while pos < len(self.code):
            match = None
            for tok_type, tok_regex in TOKEN_SPEC:
                pattern = re.compile(tok_regex)
                match = pattern.match(self.code, pos)
                if match:
                    text = match.group(0)
                    if tok_type not in ["SKIP", "NEWLINE", "COMMENT", "MCOMMENT"]:
                        self.tokens.append((tok_type, text))
                    pos = match.end(0)
                    break
            if not match:
                raise SyntaxError(f"Unknown token at {pos}")
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens): return self.tokens[self.pos]
        return None

    def advance(self): self.pos += 1

    def match(self, *token_types):
        tok = self.peek()
        if tok and tok[0] in token_types:
            self.advance()
            return tok
        return None

    def parse(self):
        statements = []
        while self.peek(): statements.append(self.statement())
        return statements

    def statement(self):
        tok = self.peek()
        if tok[0] == "ID" and tok[1] == "assign": return self.assign_stmt()
        if tok[0] == "ID" and tok[1] == "let": return self.let_stmt()
        if tok[0] == "ID" and tok[1] == "var": return self.var_stmt()
        if tok[0] == "ID" and tok[1] == "say": return self.say_stmt()
        if tok[0] == "ID" and tok[1] == "if": return self.if_stmt()
        if tok[0] == "ID" and tok[1] == "while": return self.while_stmt()
        if tok[0] == "ID" and tok[1] == "func": return self.func_def()
        if tok[0] == "ID" and tok[1] == "import": return self.import_stmt()
        return self.expr_stmt()

    def assign_stmt(self):
        self.match("ID")  # assign
        name_tok = self.match("ID")
        self.match("OP")
        expr = self.expression()
        self.match("SEMICOLON")
        return Assign(name_tok[1], expr)

    def let_stmt(self):
        self.match("ID")  # let
        name_tok = self.match("ID")
        type_annotation = None
        if self.match("COLON"):
            type_tok = self.match("ID")
            type_annotation = type_tok[1]
        self.match("OP")  # '='
        expr = self.expression()
        self.match("SEMICOLON")
        return Let(name_tok[1], expr, type_annotation)

    def var_stmt(self):
        self.match("ID")  # var
        name_tok = self.match("ID")
        type_annotation = None
        if self.match("COLON"):
            type_tok = self.match("ID")
            type_annotation = type_tok[1]
        self.match("OP")  # '='
        expr = self.expression()
        self.match("SEMICOLON")
        return VarDecl(name_tok[1], expr, type_annotation)

    def say_stmt(self):
        self.match("ID")
        expr = self.expression()
        self.match("SEMICOLON")
        return Print(expr)

    def if_stmt(self):
        self.match("ID")
        cond = self.expression()
        self.match("LBRACE")
        body = self.block()
        self.match("RBRACE")
        orelse = None
        next_tok = self.peek()
        if next_tok and next_tok[0] == "ID" and next_tok[1] == "else":
            self.match("ID")
            self.match("LBRACE")
            orelse = self.block()
            self.match("RBRACE")
        return If(cond, body, orelse)

    def while_stmt(self):
        self.match("ID")
        cond = self.expression()
        self.match("LBRACE")
        body = self.block()
        self.match("RBRACE")
        return While(cond, body)

    def func_def(self):
        self.match("ID")
        name_tok = self.match("ID")
        self.match("LPAREN")
        params = []
        while True:
            param = self.match("ID")
            if param: params.append(param[1])
            if not self.match("COMMA"): break
        self.match("RPAREN")
        self.match("LBRACE")
        body = self.block()
        self.match("RBRACE")
        return FuncDef(name_tok[1], params, body)

    def import_stmt(self):
        self.match("ID")  # import
        module_tok = self.match("ID")
        alias = None
        if self.peek() and self.peek()[0] == "ID" and self.peek()[1] == "as":
            self.match("ID")  # as
            alias_tok = self.match("ID")
            alias = alias_tok[1]
        self.match("SEMICOLON")
        return Import(module_tok[1], alias)

    def block(self):
        statements = []
        while True:
            tok = self.peek()
            if not tok or tok[0] == "RBRACE": break
            statements.append(self.statement())
        return statements

    def expr_stmt(self):
        expr = self.expression()
        self.match("SEMICOLON")
        return expr

    def expression(self): return self.binary_expr()

    def binary_expr(self, precedence=0):
        left = self.primary()
        while True:
            op = self.peek()
            if not op or op[0] != "OP": break
            self.advance()
            op_val = op[1].replace("&&", "and").replace("||", "or").replace("!", "not")
            right = self.binary_expr()
            left = BinOp(left, op_val, right)
        return left

    def primary(self):
        tok = self.peek()
        if not tok: raise SyntaxError("Unexpected end")
        if tok[0] == "NUMBER": self.advance(); return Num(float(tok[1]))
        if tok[0] == "STRING": self.advance(); return Str(tok[1][1:-1])
        if tok[0] == "ID":
            self.advance()
            if self.peek() and self.peek()[0] == "LPAREN":
                self.match("LPAREN")
                args = []
                while True:
                    if self.peek() and self.peek()[0] == "RPAREN": break
                    args.append(self.expression())
                    if not self.match("COMMA"): break
                self.match("RPAREN")
                return FuncCall(tok[1], args)
            return Var(tok[1])
        if tok[0] == "LPAREN":
            self.match("LPAREN")
            expr = self.expression()
            self.match("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected token {tok}")
