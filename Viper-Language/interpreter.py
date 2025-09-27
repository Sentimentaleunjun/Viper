from core import say, input_func

class Num:
    def __init__(self, value): self.value = value
class Str:
    def __init__(self, value): self.value = value
class Bool:
    def __init__(self, value): self.value = value
class Null:
    def __init__(self): pass
class Var:
    def __init__(self, name): self.name = name
class Assign:
    def __init__(self, name, value): self.name, self.value = name, value
class BinOp:
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
class UnaryOp:
    def __init__(self, op, expr): self.op, self.expr = op, expr
class Print:
    def __init__(self, expr): self.expr = expr
class If:
    def __init__(self, condition, body, orelse=None): self.condition, self.body, self.orelse = condition, body, orelse
class While:
    def __init__(self, condition, body): self.condition, self.body = condition, body
class FuncDef:
    def __init__(self, name, params, body): self.name, self.params, self.body = name, params, body
class FuncCall:
    def __init__(self, name, args): self.name, self.args = name, args
class Return:
    def __init__(self, value): self.value = value

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
        self.modules = {}
    def get(self, name):
        if name in self.vars: return self.vars[name]
        if self.parent: return self.parent.get(name)
        if name in self.modules: return self.modules[name]
        raise Exception(f"{name} not found")
    def set(self, name, value): self.vars[name] = value

class Interpreter:
    def eval(self, node, env):
        if isinstance(node, Num): return node.value
        if isinstance(node, Str): return node.value
        if isinstance(node, Bool): return node.value
        if isinstance(node, Null): return None
        if isinstance(node, Var): return env.get(node.name)
        if isinstance(node, Assign):
            value = self.eval(node.value, env)
            env.set(node.name, value)
            return value
        if isinstance(node, BinOp):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            if node.op == "+": return left + right
            if node.op == "-": return left - right
            if node.op == "*": return left * right
            if node.op == "/": return left / right
            if node.op == "%": return left % right
            if node.op == "==": return left == right
            if node.op == "!=": return left != right
            if node.op == "<": return left < right
            if node.op == "<=": return left <= right
            if node.op == ">": return left > right
            if node.op == ">=": return left >= right
            if node.op == "and": return left and right
            if node.op == "or": return left or right
        if isinstance(node, UnaryOp):
            val = self.eval(node.expr, env)
            if node.op == "-": return -val
            if node.op == "not": return not val
        if isinstance(node, Print):
            val = self.eval(node.expr, env)
            say(val)
        if isinstance(node, If):
            if self.eval(node.condition, env):
                for n in node.body: self.eval(n, env)
            elif node.orelse:
                for n in node.orelse: self.eval(n, env)
        if isinstance(node, While):
            while self.eval(node.condition, env):
                for n in node.body: self.eval(n, env)
        if isinstance(node, FuncDef):
            env.set(node.name, node)
        if isinstance(node, FuncCall):
            func = env.get(node.name)
            if isinstance(func, FuncDef):
                new_env = Environment(env)
                for name, val in zip(func.params, node.args):
                    new_env.set(name, self.eval(val, env))
                result = None
                for n in func.body:
                    if isinstance(n, Return):
                        result = self.eval(n.value, new_env)
                        break
                    else:
                        self.eval(n, new_env)
                return result
            elif callable(func):
                args = [self.eval(a, env) for a in node.args]
                return func(*args)
        if isinstance(node, Return):
            return self.eval(node.value, env)
