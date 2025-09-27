import os,sys
current_dir=os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.insert(0,current_dir)
from interpreter import Interpreter
from viper_parser import tokenize,parse_stmt

inter=Interpreter()
print("Viper-Lite REPL (type 'exit')")

def read_block():
    lines=[]
    while True:
        line=input("... ").rstrip()
        if line=="": break
        lines.append(line)
    return lines

while True:
    try:
        code=input("viper> ").strip()
        if code.lower()=="exit": break

        if code.startswith(("while","if","func")):
            header=code
            body_lines=read_block()
            body_nodes=[parse_stmt(tokenize(line.replace(";",""))) for line in body_lines if line.strip()]
            node=parse_stmt(tokenize(header.replace(":","")),body_nodes)
            inter.exec(node)
            continue

        for stmt_code in code.split(";"):
            stmt_code=stmt_code.strip()
            if not stmt_code: continue
            node=parse_stmt(tokenize(stmt_code))
            inter.exec(node)

    except Exception as e:
        print(f"Error: {e}")
