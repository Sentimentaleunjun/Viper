import re
from interpreter import Num, Str, Var, Assign, Print, BinOp, FuncCall, While, If, UserFunc

def tokenize(code):
    pattern = r'"[^"]*"|\(|\)|\.|=|<|>|\+|\-|\*|/|,|[^\s\(\)\.=<>+\-*/]+'
    return re.findall(pattern, code)

def parse_expr(tokens):
    if not tokens: raise Exception("Empty expression")
    if len(tokens)==1:
        t=tokens[0]
        if t.isdigit(): return Num(int(t))
        if t.startswith('"') and t.endswith('"'): return Str(t[1:-1])
        return Var(t)
    if "(" in tokens:
        idx = tokens.index("(")
        name_tokens = tokens[:idx]
        args_tokens = tokens[idx+1:-1]
        args_nodes = [parse_expr([a]) for a in args_tokens if a != ',']
        if len(name_tokens)==1:
            return FuncCall(None, name_tokens[0], args_nodes)
        elif len(name_tokens)==3 and name_tokens[1]=='.':
            return FuncCall(name_tokens[0], name_tokens[2], args_nodes)
        else:
            raise Exception("Unsupported function call")
    if len(tokens)==3:
        l, op, r = tokens
        return BinOp(parse_expr([l]), op, parse_expr([r]))
    raise Exception("Unsupported expression: " + " ".join(tokens))

def parse_stmt(tokens, body=None):
    if not tokens: raise Exception("Empty statement")
    if tokens[0]=="say":
        expr_tokens = tokens[1:]
        if expr_tokens and expr_tokens[0]=="(" and expr_tokens[-1]==")":
            expr_tokens = expr_tokens[1:-1]
        return Print(parse_expr(expr_tokens))
    if "=" in tokens:
        idx = tokens.index("=")
        return Assign(tokens[0], parse_expr(tokens[idx+1:]))
    if tokens[0]=="while":
        cond_expr = parse_expr(tokens[1:])
        return While(cond_expr, body or [])
    if tokens[0]=="if":
        cond_expr = parse_expr(tokens[1:])
        return If(cond_expr, body or [])
    if tokens[0]=="func":
        name = tokens[1]
        args = [a.strip() for a in tokens[2].split(",")] if len(tokens)>2 else []
        return Assign(name, UserFunc(args, body or []))
    raise Exception("Unknown statement: " + " ".join(tokens))
