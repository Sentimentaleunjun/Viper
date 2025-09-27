import socket, hashlib, urllib.request, copy

class Num:
    def __init__(self, value): self.value = value
    def eval(self, env): return self.value

class Str:
    def __init__(self, value): self.value = value
    def eval(self, env): return self.value

class Var:
    def __init__(self, name): self.name = name
    def eval(self, env):
        if self.name in env: return env[self.name]
        raise NameError(f"Variable '{self.name}' is not defined")

class Assign:
    def __init__(self, name, expr): self.name=name; self.expr=expr
    def eval(self, env):
        env[self.name] = self.expr.eval(env)
        return env[self.name]

class Print:
    def __init__(self, expr): self.expr=expr
    def eval(self, env):
        val = self.expr.eval(env)
        print(val)
        return val

class BinOp:
    def __init__(self, left, op, right): self.left=left; self.op=op; self.right=right
    def eval(self, env):
        l = self.left.eval(env)
        r = self.right.eval(env)
        if self.op=='+': return l+r
        if self.op=='-': return l-r
        if self.op=='*': return l*r
        if self.op=='/': return l//r
        if self.op=='<': return l<r
        if self.op=='>': return l>r
        if self.op=='==': return l==r
        raise Exception(f"Unknown operator {self.op}")

class FuncCall:
    def __init__(self, obj, func, args):
        self.obj=obj; self.func=func; self.args=args
    def eval(self, env):
        if self.obj:
            obj_instance = env.get(self.obj)
            if not obj_instance: raise Exception(f"Object '{self.obj}' not found")
            func_instance = getattr(obj_instance, self.func, None)
            if not callable(func_instance):
                raise Exception(f"Function '{self.obj}.{self.func}' not defined")
        else:
            func_instance = env.get(self.func)
            if isinstance(env.get(self.func), UserFunc):
                return env[self.func].call([a.eval(env) for a in self.args], env)
            elif callable(func_instance):
                pass
            else:
                raise Exception(f"Function '{self.func}' not defined")
        arg_vals = [a.eval(env) for a in self.args]
        return func_instance(*arg_vals)

class While:
    def __init__(self, cond_expr, body): self.cond_expr=cond_expr; self.body=body
    def eval(self, env):
        while self.cond_expr.eval(env):
            for stmt in self.body: stmt.eval(env)

class If:
    def __init__(self, cond_expr, body, else_body=None):
        self.cond_expr=cond_expr; self.body=body; self.else_body=else_body
    def eval(self, env):
        if self.cond_expr.eval(env):
            for stmt in self.body: stmt.eval(env)
        elif self.else_body:
            for stmt in self.else_body: stmt.eval(env)

class UserFunc:
    def __init__(self, args, body): self.args=args; self.body=body
    def call(self, arg_vals, env):
        local_env = copy.deepcopy(env)
        for a,v in zip(self.args,arg_vals): local_env[a]=v
        for stmt in self.body: stmt.eval(local_env)
        return None

class Interpreter:
    def __init__(self):
        self.env = {
            "network": NetworkModule(),
            "dns": DNSModule(),
            "security": SecurityModule()
        }
    def exec(self, node): return node.eval(self.env)

class NetworkModule:
    def get_ip(self, host): return socket.gethostbyname(host)
    def http_get(self, url):
        with urllib.request.urlopen(url) as resp: return resp.read().decode()

class DNSModule:
    def lookup(self, domain): return socket.gethostbyname_ex(domain)

class SecurityModule:
    def sha256(self, msg):
        return hashlib.sha256(msg.encode()).hexdigest()
