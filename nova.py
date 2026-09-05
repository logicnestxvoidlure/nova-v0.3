import sys
import math
import json
import re
import traceback

VERSION = "3.0.0"

class NovaError(Exception):
    pass

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass

class ThrowSignal(Exception):
    def __init__(self, value):
        self.value = value

class Token:
    def __init__(self, kind, value, line, col):
        self.kind = kind
        self.value = value
        self.line = line
        self.col = col
    def __repr__(self):
        return f"{self.kind}({self.value!r})@{self.line}:{self.col}"

class Lexer:
    keywords = {
        "let","const","fn","return","if","else","while","for","in","break",
        "continue","true","false","null","class","extends","new","this",
        "try","catch","finally","throw","import","as"
    }
    two = {"==","!=","<=",">=","&&","||","+=","-=","*=","/=","%=","**","->",".."}
    one = set("+-*/%=<>!.,:;(){}[]")

    def __init__(self, text):
        self.text = text
        self.i = 0
        self.line = 1
        self.col = 1

    def advance(self):
        ch = self.text[self.i]
        self.i += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def tokenize(self):
        out = []
        while self.i < len(self.text):
            ch = self.text[self.i]
            if ch.isspace():
                self.advance()
                continue
            if ch == "/" and self.i + 1 < len(self.text) and self.text[self.i+1] == "/":
                while self.i < len(self.text) and self.text[self.i] != "\n":
                    self.advance()
                continue
            line, col = self.line, self.col
            if ch in "\"'":
                quote = self.advance()
                s = ""
                while self.i < len(self.text):
                    c = self.advance()
                    if c == quote:
                        break
                    if c == "\\":
                        if self.i >= len(self.text):
                            raise NovaError(f"Unterminated string at {line}:{col}")
                        e = self.advance()
                        s += {"n":"\n","t":"\t","r":"\r","\\":"\\","\"":"\"","'":"'"} .get(e,e)
                    else:
                        s += c
                else:
                    raise NovaError(f"Unterminated string at {line}:{col}")
                out.append(Token("STRING",s,line,col))
                continue
            if ch.isdigit() or (ch == "." and self.i + 1 < len(self.text) and self.text[self.i+1].isdigit()):
                raw = ""
                dots = 0
                while self.i < len(self.text) and (self.text[self.i].isdigit() or self.text[self.i] == "."):
                    c = self.advance()
                    raw += c
                    if c == ".":
                        dots += 1
                if dots > 1:
                    raise NovaError(f"Invalid number at {line}:{col}")
                value = float(raw) if "." in raw else int(raw)
                out.append(Token("NUMBER",value,line,col))
                continue
            if ch.isalpha() or ch == "_":
                raw = ""
                while self.i < len(self.text) and (self.text[self.i].isalnum() or self.text[self.i] == "_"):
                    raw += self.advance()
                out.append(Token("KW" if raw in self.keywords else "IDENT",raw,line,col))
                continue
            pair = self.text[self.i:self.i+2]
            if pair in self.two:
                self.advance(); self.advance()
                out.append(Token("OP",pair,line,col))
                continue
            if ch in self.one:
                self.advance()
                out.append(Token("OP",ch,line,col))
                continue
            raise NovaError(f"Unexpected character {ch!r} at {line}:{col}")
        out.append(Token("EOF","",self.line,self.col))
        return out

class Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0

    def cur(self):
        return self.t[self.i]

    def peek(self, n=1):
        return self.t[min(self.i+n, len(self.t)-1)]

    def match(self, value):
        if self.cur().value == value:
            x = self.cur()
            self.i += 1
            return x
        return None

    def expect(self, value):
        x = self.match(value)
        if not x:
            c = self.cur()
            raise NovaError(f"Expected {value!r} at {c.line}:{c.col}, got {c.value!r}")
        return x

    def ident(self):
        x = self.cur()
        if x.kind not in ("IDENT","KW"):
            raise NovaError(f"Expected identifier at {x.line}:{x.col}")
        self.i += 1
        return x.value

    def program(self):
        body = []
        while self.cur().kind != "EOF":
            body.append(self.statement())
            self.match(";")
        return ("program",body)

    def block(self):
        self.expect("{")
        body = []
        while self.cur().value != "}":
            if self.cur().kind == "EOF":
                raise NovaError("Unclosed block")
            body.append(self.statement())
            self.match(";")
        self.expect("}")
        return body

    def statement(self):
        c = self.cur().value
        if c in ("let","const"):
            self.i += 1
            name = self.ident()
            self.expect("=")
            return ("declare",name,self.expr(),c=="const")
        if c == "fn":
            self.i += 1
            name = self.ident()
            params = self.params()
            return ("fn",name,params,self.block())
        if c == "return":
            self.i += 1
            if self.cur().value in (";","}"):
                return ("return",("lit",None))
            return ("return",self.expr())
        if c == "if":
            self.i += 1
            cond = self.expr()
            yes = self.block()
            no = []
            if self.match("else"):
                no = self.block()
            return ("if",cond,yes,no)
        if c == "while":
            self.i += 1
            return ("while",self.expr(),self.block())
        if c == "for":
            self.i += 1
            name = self.ident()
            self.expect("in")
            return ("for",name,self.expr(),self.block())
        if c == "break":
            self.i += 1
            return ("break",)
        if c == "continue":
            self.i += 1
            return ("continue",)
        if c == "throw":
            self.i += 1
            return ("throw",self.expr())
        if c == "try":
            self.i += 1
            yes = self.block()
            name = None
            no = []
            final = []
            if self.match("catch"):
                self.expect("(")
                name = self.ident()
                self.expect(")")
                no = self.block()
            if self.match("finally"):
                final = self.block()
            return ("try",yes,name,no,final)
        if c == "class":
            return self.class_decl()
        if c == "import":
            self.i += 1
            path = self.cur().value
            if self.cur().kind != "STRING":
                raise NovaError("Import path must be a string")
            self.i += 1
            alias = None
            if self.match("as"):
                alias = self.ident()
            return ("import",path,alias)
        if c == "{":
            return ("block",self.block())
        return ("expr",self.expr())

    def class_decl(self):
        self.expect("class")
        name = self.ident()
        parent = None
        if self.match("extends"):
            parent = self.ident()
        self.expect("{")
        methods = []
        while self.cur().value != "}":
            self.expect("fn")
            mn = self.ident()
            params = self.params()
            methods.append((mn,params,self.block()))
            self.match(";")
        self.expect("}")
        return ("class",name,parent,methods)

    def params(self):
        self.expect("(")
        p = []
        if self.cur().value != ")":
            while True:
                p.append(self.ident())
                if not self.match(","):
                    break
        self.expect(")")
        return p

    def expr(self):
        return self.assign()

    def assign(self):
        x = self.logic_or()
        if self.cur().value in ("=","+=","-=","*=","/=","%="):
            op = self.cur().value
            self.i += 1
            return ("assign",op,x,self.assign())
        return x

    def logic_or(self):
        x = self.logic_and()
        while self.match("||"):
            x = ("bin","||",x,self.logic_and())
        return x

    def logic_and(self):
        x = self.equality()
        while self.match("&&"):
            x = ("bin","&&",x,self.equality())
        return x

    def equality(self):
        x = self.compare()
        while self.cur().value in ("==","!="):
            op=self.cur().value; self.i+=1
            x=("bin",op,x,self.compare())
        return x

    def compare(self):
        x=self.term()
        while self.cur().value in ("<","<=",">",">="):
            op=self.cur().value; self.i+=1
            x=("bin",op,x,self.term())
        return x

    def term(self):
        x=self.factor()
        while self.cur().value in ("+","-"):
            op=self.cur().value; self.i+=1
            x=("bin",op,x,self.factor())
        return x

    def factor(self):
        x=self.power()
        while self.cur().value in ("*","/","%"):
            op=self.cur().value; self.i+=1
            x=("bin",op,x,self.power())
        return x

    def power(self):
        x=self.unary()
        if self.match("**"):
            x=("bin","**",x,self.power())
        return x

    def unary(self):
        if self.cur().value in ("!","-","+"):
            op=self.cur().value; self.i+=1
            return ("unary",op,self.unary())
        return self.postfix()

    def postfix(self):
        x=self.primary()
        while True:
            if self.match("("):
                args=[]
                if self.cur().value != ")":
                    while True:
                        args.append(self.expr())
                        if not self.match(","):
                            break
                self.expect(")")
                x=("call",x,args)
            elif self.match("["):
                idx=self.expr()
                self.expect("]")
                x=("index",x,idx)
            elif self.match("."):
                x=("get",x,self.ident())
            else:
                break
        return x

    def primary(self):
        c=self.cur()
        if c.kind == "NUMBER":
            self.i+=1; return ("lit",c.value)
        if c.kind == "STRING":
            self.i+=1; return ("str",c.value)
        if c.value in ("true","false","null"):
            self.i+=1; return ("lit",{"true":True,"false":False,"null":None}[c.value])
        if c.kind in ("IDENT","KW"):
            self.i+=1
            if c.value == "fn":
                params=self.params()
                return ("lambda",params,self.block())
            if c.value == "new":
                name=self.ident()
                args=[]
                self.expect("(")
                if self.cur().value != ")":
                    while True:
                        args.append(self.expr())
                        if not self.match(","): break
                self.expect(")")
                return ("new",name,args)
            if c.value == "this":
                return ("this",)
            return ("var",c.value)
        if self.match("("):
            x=self.expr(); self.expect(")"); return x
        if self.match("["):
            vals=[]
            if self.cur().value != "]":
                while True:
                    vals.append(self.expr())
                    if not self.match(","): break
            self.expect("]")
            return ("array",vals)
        if self.match("{"):
            pairs=[]
            if self.cur().value != "}":
                while True:
                    k=self.cur()
                    if k.kind not in ("IDENT","STRING","NUMBER","KW"):
                        raise NovaError("Invalid map key")
                    self.i+=1
                    self.expect(":")
                    pairs.append((str(k.value),self.expr()))
                    if not self.match(","): break
            self.expect("}")
            return ("map",pairs)
        raise NovaError(f"Unexpected token {c.value!r} at {c.line}:{c.col}")

class Env:
    def __init__(self,parent=None):
        self.values={}
        self.consts=set()
        self.parent=parent
    def define(self,k,v,const=False):
        self.values[k]=v
        if const:self.consts.add(k)
    def find(self,k):
        if k in self.values:return self
        if self.parent:return self.parent.find(k)
        return None
    def get(self,k):
        e=self.find(k)
        if not e: raise NovaError(f"Undefined variable: {k}")
        return e.values[k]
    def set(self,k,v):
        e=self.find(k)
        if not e: raise NovaError(f"Undefined variable: {k}")
        if k in e.consts: raise NovaError(f"Cannot modify constant: {k}")
        e.values[k]=v

class NovaFunction:
    def __init__(self,name,params,body,env):
        self.name=name; self.params=params; self.body=body; self.env=env
    def call(self,args):
        e=Env(self.env)
        for i,p in enumerate(self.params):
            e.define(p,args[i] if i<len(args) else None)
        try:
            Interpreter().exec_block(self.body,e)
        except ReturnSignal as r:
            return r.value
        return None
    def __repr__(self):
        return f"<fn {self.name}>"

class NovaClass:
    def __init__(self,name,parent,methods):
        self.name=name; self.parent=parent; self.methods=methods
    def method(self,name):
        if name in self.methods:return self.methods[name]
        if self.parent:return self.parent.method(name)
        return None

class NovaObject:
    def __init__(self,cls):
        self.cls=cls; self.fields={}
    def get(self,name):
        if name in self.fields:return self.fields[name]
        fn=self.cls.method(name)
        if fn:
            def bound(*args):
                e=Env(fn.env)
                e.define("this",self)
                for i,p in enumerate(fn.params):
                    e.define(p,args[i] if i<len(args) else None)
                try: Interpreter().exec_block(fn.body,e)
                except ReturnSignal as r:return r.value
                return None
            return bound
        raise NovaError(f"Unknown property {name}")
    def set(self,name,value):
        self.fields[name]=value

class Compiler:
    def __init__(self):
        self.code=[]
    def emit(self,op,arg=None):
        self.code.append((op,arg))
    def compile(self,node):
        k=node[0]
        if k=="program":
            for s in node[1]:self.compile(s)
            self.emit("HALT")
        elif k=="lit":
            self.emit("PUSH",node[1])
        elif k=="str":
            self.emit("PUSH",node[1])
        elif k=="var":
            self.emit("LOAD",node[1])
        elif k=="bin":
            self.compile(node[2]);self.compile(node[3]);self.emit("BIN",node[1])
        elif k=="unary":
            self.compile(node[2]);self.emit("UNARY",node[1])
        elif k=="array":
            for x in node[1]:self.compile(x)
            self.emit("ARRAY",len(node[1]))
        elif k=="expr":
            self.compile(node[1]);self.emit("POP")
        elif k=="declare":
            self.compile(node[2]);self.emit("STORE",node[1])
        else:
            self.emit("INTERPRET",node)

class VM:
    def __init__(self,env):
        self.env=env
        self.stack=[]
    def run(self,code):
        ip=0
        while ip<len(code):
            op,arg=code[ip];ip+=1
            if op=="HALT":break
            if op=="PUSH":self.stack.append(arg)
            elif op=="POP":self.stack.pop()
            elif op=="LOAD":self.stack.append(self.env.get(arg))
            elif op=="STORE":self.env.define(arg,self.stack.pop())
            elif op=="ARRAY":
                n=arg; vals=self.stack[-n:] if n else []; del self.stack[len(self.stack)-n:] if n else self.stack[:0]
                self.stack.append(vals)
            elif op=="UNARY":
                a=self.stack.pop()
                self.stack.append(Interpreter().unary(arg,a))
            elif op=="BIN":
                b=self.stack.pop();a=self.stack.pop()
                self.stack.append(Interpreter().binary(arg,a,b))
            elif op=="INTERPRET":
                Interpreter().exec_stmt(arg,self.env)

class Interpreter:
    def truth(self,v): return bool(v)
    def unary(self,op,a):
        if op=="!":return not self.truth(a)
        if op=="-":return -a
        if op=="+":return +a
        raise NovaError("Bad unary operator")
    def binary(self,op,a,b):
        if op=="+": return a+b
        if op=="-": return a-b
        if op=="*": return a*b
        if op=="/": return a/b
        if op=="%": return a%b
        if op=="**": return a**b
        if op=="==": return a==b
        if op=="!=": return a!=b
        if op=="<": return a<b
        if op=="<=": return a<=b
        if op==">": return a>b
        if op==">=": return a>=b
        if op=="&&": return self.truth(a) and self.truth(b)
        if op=="||": return self.truth(a) or self.truth(b)
        raise NovaError(f"Unknown operator {op}")
    def eval(self,n,e):
        k=n[0]
        if k=="lit":return n[1]
        if k=="str":
            return re.sub(r"\$\{([^}]+)\}",lambda m:str(self.eval(Parser(Lexer(m.group(1)).tokenize()).expr(),e)),n[1])
        if k=="var":return e.get(n[1])
        if k=="this":return e.get("this")
        if k=="array":return [self.eval(x,e) for x in n[1]]
        if k=="map":return {k:self.eval(v,e) for k,v in n[1]}
        if k=="bin":
            a=self.eval(n[2],e)
            if n[1]=="&&" and not self.truth(a):return False
            if n[1]=="||" and self.truth(a):return True
            return self.binary(n[1],a,self.eval(n[3],e))
        if k=="unary":return self.unary(n[1],self.eval(n[2],e))
        if k=="call":
            fn=self.eval(n[1],e); args=[self.eval(x,e) for x in n[2]]
            if not callable(fn):raise NovaError("Value is not callable")
            return fn(*args)
        if k=="index":
            return self.eval(n[1],e)[self.eval(n[2],e)]
        if k=="get":
            obj=self.eval(n[1],e); name=n[2]
            if isinstance(obj,NovaObject):return obj.get(name)
            if isinstance(obj,dict):return obj.get(name)
            return getattr(obj,name)
        if k=="assign":
            target=n[2]; value=self.eval(n[3],e)
            if target[0]=="var":
                if n[1]=="=":e.set(target[1],value) if e.find(target[1]) else e.define(target[1],value)
                else:
                    old=e.get(target[1]); e.set(target[1],self.binary(n[1][0],old,value))
                return value
            if target[0]=="index":
                obj=self.eval(target[1],e); idx=self.eval(target[2],e); 
                if n[1]!="=":value=self.binary(n[1][0],obj[idx],value)
                obj[idx]=value; return value
            if target[0]=="get":
                obj=self.eval(target[1],e); name=target[2]
                if isinstance(obj,NovaObject):obj.set(name,value)
                else:obj[name]=value
                return value
        if k=="lambda":return NovaFunction("<lambda>",n[1],n[2],e)
        if k=="new":
            cls=e.get(n[1]); obj=NovaObject(cls)
            init=cls.method("init")
            if init:
                obj.get("init")(*[self.eval(x,e) for x in n[2]])
            return obj
        raise NovaError(f"Unknown expression {k}")
    def exec_stmt(self,n,e):
        k=n[0]
        if k=="expr":self.eval(n[1],e)
        elif k=="declare":e.define(n[1],self.eval(n[2],e),n[3])
        elif k=="return":raise ReturnSignal(self.eval(n[1],e))
        elif k=="fn":e.define(n[1],NovaFunction(n[1],n[2],n[3],e))
        elif k=="if":
            self.exec_block(n[2] if self.truth(self.eval(n[1],e)) else n[3],e)
        elif k=="while":
            guard=0
            while self.truth(self.eval(n[1],e)):
                guard+=1
                if guard>1000000:raise NovaError("Loop limit exceeded")
                try:self.exec_block(n[2],e)
                except BreakSignal:break
                except ContinueSignal:continue
        elif k=="for":
            seq=self.eval(n[2],e)
            for x in seq:
                e.define(n[1],x) if not e.find(n[1]) else e.set(n[1],x)
                try:self.exec_block(n[3],e)
                except BreakSignal:break
                except ContinueSignal:continue
        elif k=="break":raise BreakSignal()
        elif k=="continue":raise ContinueSignal()
        elif k=="throw":raise ThrowSignal(self.eval(n[1],e))
        elif k=="try":
            try:self.exec_block(n[1],e)
            except ThrowSignal as x:
                if n[2]:e.define(n[2],x.value)
                self.exec_block(n[3],e)
            finally:
                self.exec_block(n[4],e)
        elif k=="block":self.exec_block(n[1],e)
        elif k=="class":
            parent=e.get(n[2]) if n[2] else None
            methods={}
            for name,params,body in n[3]:
                methods[name]=NovaFunction(name,params,body,e)
            e.define(n[1],NovaClass(n[1],parent,methods))
        elif k=="import":
            path=n[1]
            if not path.endswith(".nova"):path+=".nova"
            if not path.startswith(".") and "/" not in path and "\\" not in path:
                path=path
            with open(path,"r",encoding="utf8") as f:
                ast=Parser(Lexer(f.read()).tokenize()).program()
            mod=Env(e);self.exec_block(ast[1],mod)
            name=n[2] or path.rsplit("/",1)[-1].rsplit("\\",1)[-1].replace(".nova","")
            e.define(name,mod.values)
    def exec_block(self,body,e):
        for s in body:self.exec_stmt(s,e)

def builtins():
    e=Env()
    e.define("print",lambda *x: print(*x))
    e.define("input",lambda prompt="":input(str(prompt)))
    e.define("len",lambda x:len(x))
    e.define("type",lambda x: type(x).__name__)
    e.define("str",lambda x: str(x))
    e.define("num",lambda x: float(x) if "." in str(x) else int(x))
    e.define("bool",lambda x: bool(x))
    e.define("range",lambda a,b=None,step=1: list(range(a,b,step)) if b is not None else list(range(a)))
    e.define("sqrt",math.sqrt);e.define("abs",abs);e.define("floor",math.floor)
    e.define("ceil",math.ceil);e.define("round",round);e.define("min",min);e.define("max",max)
    e.define("read_file",lambda p:open(p,"r",encoding="utf8").read())
    e.define("write_file",lambda p,c:open(p,"w",encoding="utf8").write(str(c)))
    e.define("append_file",lambda p,c:open(p,"a",encoding="utf8").write(str(c)))
    e.define("json_encode",lambda x:json.dumps(x))
    e.define("json_decode",lambda x:json.loads(x))
    e.define("version",VERSION)
    return e

def parse(src):
    return Parser(Lexer(src).tokenize()).program()

def run(src,env=None):
    ast=parse(src)
    env=env or builtins()
    Interpreter().exec_block(ast[1],env)
    return env

def dump_ast(node,level=0):
    if isinstance(node,tuple):
        print("  "*level + node[0])
        for x in node[1:]:dump_ast(x,level+1)
    elif isinstance(node,list):
        for x in node:dump_ast(x,level+1)

def repl():
    env=builtins()
    print(f"Nova {VERSION} REPL")
    print("Type exit to quit")
    while True:
        try:
            s=input("nova> ")
            if s.strip()=="exit":break
            if not s.strip():continue
            run(s,env)
        except Exception as ex:
            print("Error:",ex)

def main():
    args=sys.argv[1:]
    if not args:
        repl();return
    if args[0] in ("-v","--version"):
        print(VERSION);return
    mode=None
    if args[0].startswith("--"):
        mode=args.pop(0)
    if not args:
        print("Nova: missing source file");return
    path=args[0]
    with open(path,"r",encoding="utf8") as f:src=f.read()
    try:
        ast=parse(src)
        if mode=="--tokens":
            for t in Lexer(src).tokenize():print(t)
        elif mode=="--ast":
            dump_ast(ast)
        elif mode=="--check":
            print("OK")
        else:
            env=builtins()
            Compiler().compile(ast)
            Interpreter().exec_block(ast[1],env)
    except Exception as ex:
        print(f"NovaError: {ex}")
        if "--trace" in args:traceback.print_exc()
        sys.exit(1)

if __name__=="__main__":
    main()
