import sys
from parser import Lexer, Parser
from interpreter import Interpreter, Environment
from core import say, input_func
from modules import network, dns, security

def run_file(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens).parse()
    env = Environment()
    env.modules.update({"network": network, "dns": dns, "security": security, "say": say, "input": input_func})
    Interpreter().eval(ast[0], env)

def repl():
    env = Environment()
    env.modules.update({"network": network, "dns": dns, "security": security, "say": say, "input": input_func})
    while True:
        try:
            text = input("Viper> ")
            tokens = Lexer(text).tokenize()
            ast = Parser(tokens).parse()
            Interpreter().eval(ast[0], env)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()
