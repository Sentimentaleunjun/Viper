class Num:
    def __init__(self,value): self.value=value
class Str:
    def __init__(self,value): self.value=value
class Var:
    def __init__(self,name): self.name=name
class BinOp:
    def __init__(self,left,op,right): self.left,self.op,self.right=left,op,right
class Assign:
    def __init__(self,name,expr): self.name,self.expr=name,expr
class Print:
    def __init__(self,expr): self.expr=expr
class If:
    def __init__(self,cond,then,els=None): self.cond,self.then,self.els=cond,then,els
class While:
    def __init__(self,cond,body): self.cond,self.body=cond,body
class Function:
    def __init__(self,name,params,body): self.name,self.params,self.body=name,params,body
class Return:
    def __init__(self,value): self.value=value
class Call:
    def __init__(self,name,args): self.name,self.args=name,args
class Thing:
    def __init__(self):
        self.props = {}
        self.methods = {}
class AttrCall:
    def __init__(self,obj,method,args): self.obj,self.method,self.args=obj,method,args
class Import:
    def __init__(self,name): self.name=name

class Interpreter:
    def __init__(self):
        self.env = {}
        self.funcs = {}
        self.modules = {}

    def eval(self,node):
        if isinstance(node,Num): return node.value
        if isinstance(node,Str): return node.value
        if isinstance(node,Var): return self.env.get(node.name,0)
        if isinstance(node,BinOp):
            l,r=self.eval(node.left),self.eval(node.right)
            if node.op=="+": return l+r
            if node.op=="-": return l-r
            if node.op=="*": return l*r
            if node.op=="/": return l/r
            if node.op==">": return l>r
            if node.op=="<": return l<r
            if node.op=="==": return l==r
            if node.op=="!=": return l!=r
        if isinstance(node,Assign):
            val=self.eval(node.expr) if node.expr else 0
            self.env[node.name]=val
        if isinstance(node,Print): print(self.eval(node.expr))
        if isinstance(node,If):
            if self.eval(node.cond): [self.eval(s) for s in node.then]
            elif node.els: [self.eval(s) for s in node.els]
        if isinstance(node,While):
            while self.eval(node.cond): [self.eval(s) for s in node.body]
        if isinstance(node,Function):
            self.funcs[node.name]=node
        if isinstance(node,Return):
            raise Exception(self.eval(node.value))
        if isinstance(node,Call):
            if node.name in self.funcs:
                fn=self.funcs[node.name]
                saved=self.env.copy()
                for p,a in zip(fn.params,node.args): self.env[p]=self.eval(a)
                try:
                    for s in fn.body: self.eval(s)
                    result=None
                except Exception as e:
                    result=e.args[0]
                self.env=saved
                return result
        if isinstance(node,Thing): return node
        if isinstance(node,AttrCall):
            obj=self.eval(node.obj)
            if node.method in obj.methods:
                fn=obj.methods[node.method]
                saved=self.env.copy()
                for p,a in zip(fn.params,node.args): self.env[p]=self.eval(a)
                try:
                    for s in fn.body: self.eval(s)
                    result=None
                except Exception as e:
                    result=e.args[0]
                self.env=saved
                return result
        if isinstance(node,Import):
            mod_name=node.name
            if mod_name not in self.modules:
                self.modules[mod_name]=Interpreter()
                with open(mod_name+".vp","r",encoding="utf-8") as f:
                    code=f.read()
                tokens=tokenize(code)
                parser=Parser(tokens)
                stmts=[]
                while parser.peek(): stmts.append(parser.parse_stmt())
                for s in stmts: self.modules[mod_name].eval(s)
            self.env[mod_name]=self.modules[mod_name].env
