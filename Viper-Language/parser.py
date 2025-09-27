import re
from interpreter import *

TOKEN_SPEC = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r'"[^"]*"'),
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OP", r"[+\-*/%]|==|!=|<=|>=|<|>"),
    ("ASSIGN", r"="),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
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
                    if tok_type != "SKIP" and tok_type != "NEWLINE":
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
    
    def parse(self):
        # TODO: 완전한 AST 변환
        # 지금은 단일 숫자/문자열 반환 테스트용
        if self.tokens[self.pos][0] == "NUMBER":
            val = float(self.tokens[self.pos][1])
            self.pos += 1
            return [Num(val)]
        elif self.tokens[self.pos][0] == "STRING":
            val = self.tokens[self.pos][1][1:-1]
            self.pos += 1
            return [Str(val)]
        else:
            raise SyntaxError("Unexpected token")
