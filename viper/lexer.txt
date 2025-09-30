import re

TOKENS = [
    ("NUMBER",   r"\d+"),
    ("STRING",   r"\".*?\""),
    ("IDENT",    r"[A-Za-z_][A-Za-z0-9_]*"),
    ("ASSIGN",   r"="),
    ("PLUS",     r"\+"),
    ("MINUS",    r"-"),
    ("MUL",      r"\*"),
    ("DIV",      r"/"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("LBRACE",   r"\{"),
    ("RBRACE",   r"\}"),
    ("SEMICOLON",r";"),
    ("WS",       r"[ \t\n]+"),
]

def tokenize(code: str):
    tokens = []
    while code:
        match = None
        for ttype, pattern in TOKENS:
            regex = re.match(pattern, code)
            if regex:
                match = regex.group(0)
                if ttype != "WS":
                    tokens.append((ttype, match))
                code = code[len(match):]
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens
