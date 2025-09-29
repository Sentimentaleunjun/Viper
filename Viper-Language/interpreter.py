# interpreter.py
from core import say, input_func
import dns, network, security

# --------------------------
# AST Node 정의
# --------------------------
class Num:       # 숫자
    def __init__(self, value): self.value = value

class Str:       # 문자열
    def __init__(self, value): self.value = value

class Bool:      # 불리언
    def __init__(self, value): self.value = value

class Null:      # 널
    def __init__(self): pass

class Var:       # 변수 참조
    def __init__(self, name): self.name = name

class Assign:    # assign
    def __init__(self, name, value): self.name, self.value = name, value

class Let:       # let (상수/타입 지정 변수)
    def __init__(self, name, value, vtype=None):
        self.name, self.value, self.vtype = name, value, vtype

class VarDef:    # var (mutable 특수 변수)
    def __init__(self, name, value, vtype=None):
        self.name, self.value, self.vtype = name, value, vtype

class BinOp:     # 이항 연산
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right

class UnaryOp:   # 단항 연산
    def __init__(self, op, expr): self.op, self.expr = op, expr

class Print:     # 출력
    def __init__(self, expr): self.expr = expr

class If:        # 조건문
    def __init__(self, condition, body, orelse=None):
        self.condition, self.body, self.orelse = condition, body, orelse

class While:     # 반복문
    def __init__(self, condition, body):
        self.condition, self.body = condition, body

class FuncDef:   # 함수 정의
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body

class FuncCall:  # 함수 호출
    def __init__(self, name, args): self.name, self.args = name, args

class Return:    # 반환
    def __init__(self, value): self.value = value

class Import:    # 모듈 import
    def __init__(self, module, alias=None):
        self.module, self.alias = module, alias

class TryCatch:  # 예외 처리
    def __init__(self, try_body, err_name, catch_body):
        self.try_body, self.err_name, self.catch_body = try_body, err_name, catch_body

# --------------------------
# 환경(Environment)
# --------------------------
class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.consts = set()
        self.parent = parent
        self.modules = {}

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if name in self.modules:
            return self.modules[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"{name} not found")

    def set(self, name, value, const=False):
        if name in self.consts:
            raise Exception(f"Cannot reassign constant {name}")
        self.vars[name] = value
        if const:
            self.consts.add(name)

# --------------------------
# 인터프리터
# --------------------------
class Interpreter:
    def eval(self, node, env):
        # 리터럴
        if isinstance(node, Num): return node.value
        if isinstance(node, Str): return node.value
        if isinstance(node, Bool): return node.value
        if isinstance(node, Null): return None

        # 변수
        if isinstance(node, Var): return env.get(node.name)
        if isinstance(node, Assign):
            value = self.eval(node.value, env)
            env.set(node.name, value)
            return value
        if isinstance(node, Let):
            value = self.eval(node.value, env)
            env.set(node.name, value, const=True)
            return value
        if isinstance(node, VarDef):
            value = self.eval(node.value, env)
            env.set(node.name, value)
            return value

        # 연산자
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
            if node.op in ("and", "&&"): return left and right
            if node.op in ("or", "||"): return left or right
        if isinstance(node, UnaryOp):
            val = self.eval(node.expr, env)
            if node.op == "-": return -val
            if node.op in ("not", "!"): return not val

        # 출력
        if isinstance(node, Print):
            val = self.eval(node.expr, env)
            say(val)

        # 조건문
        if isinstance(node, If):
            if self.eval(node.condition, env):
                for n in node.body: self.eval(n, env)
            elif node.orelse:
                for n in node.orelse: self.eval(n, env)

        # 반복문
        if isinstance(node, While):
            while self.eval(node.condition, env):
                for n in node.body: self.eval(n, env)

        # 함수
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

        # 반환
        if isinstance(node, Return):
            return self.eval(node.value, env)

        # 모듈 import
        if isinstance(node, Import):
            if node.module == "dns":
                env.modules[node.alias or "dns"] = dns
            elif node.module == "network":
                env.modules[node.alias or "network"] = network
            elif node.module == "security":
                env.modules[node.alias or "security"] = security
            else:
                raise Exception(f"Unknown module {node.module}")

        # 예외 처리
        if isinstance(node, TryCatch):
            try:
                for n in node.try_body:
                    self.eval(n, env)
            except Exception as e:
                new_env = Environment(env)
                new_env.set(node.err_name, e)
                for n in node.catch_body:
                    self.eval(n, new_env)
