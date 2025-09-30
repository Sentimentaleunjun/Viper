import sys
from viper.lexer import Lexer
from viper.parser import Parser
from viper.interpreter import Interpreter, Environment
from viper.runtime import core, network, dns, security

def run_file(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens).parse()
    env = Environment()
    env.modules.update({
        "core": core,
        "network": network,
        "dns": dns,
        "security": security,
        "say": core.say,
        "input": core.input_func,
    })
    for n in ast:
        Interpreter().eval(n, env)

def repl():
    env = Environment()
    env.modules.update({
        "core": core,
        "network": network,
        "dns": dns,
        "security": security,
        "say": core.say,
        "input": core.input_func,
    })
    while True:
        try:
            text = input("Viper> ")
            tokens = Lexer(text).tokenize()
            ast = Parser(tokens).parse()
            for n in ast:
                Interpreter().eval(n, env)
        except Exception as e:
            print("Error:", e)

def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()
