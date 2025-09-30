from .lexer import tokenize
from .parser import parse
from .interpreter import eval_ast

def run(code: str):
    tokens = tokenize(code)
    ast = parse(tokens)
    eval_ast(ast)
