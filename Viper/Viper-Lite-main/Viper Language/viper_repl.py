from interpreter import Interpreter
from viper_parser import tokenize, Parser

interp = Interpreter()

while True:
    try:
        code = input("viper> ")
        if code.strip() in ('exit','quit'): break
        tokens = tokenize(code)
        parser = Parser(tokens)
        stmts = []
        while parser.peek(): stmts.append(parser.parse_stmt())
        for s in stmts: interp.eval(s)
    except Exception as e:
        print("Error:", e)
