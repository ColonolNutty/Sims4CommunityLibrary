"""
Decompiler for Python3.7.
Decompile a module or a function using the decompile() function

>>> from unpyc3 import decompile
>>> def foo(x, y, z=3, *args):
...    global g
...    for i, j in zip(x, y):
...        if z == i + j or args[i] == j:
...            g = i, j
...            return
...    
>>> print(decompile(foo))

def foo(x, y, z=3, *args):
    global g
    for i, j in zip(x, y):
        if z == i + j or args[i] == j:
            g = i, j
            return
>>>
"""
from __future__ import annotations

from typing import Union

__all__ = ['decompile']


def set_trace(trace_function):
    global current_trace
    current_trace = trace_function if trace_function else _trace


def get_trace():
    global current_trace
    return None if current_trace == _trace else current_trace


def trace(*args):
    global current_trace
    if current_trace:
        current_trace(*args)


def _trace(*args):
    pass


current_trace = _trace

# TODO:
# - Support for keyword-only arguments
# - Handle assert statements better
# - (Partly done) Nice spacing between function/class declarations

import dis
from array import array
from opcode import opname, opmap, HAVE_ARGUMENT, cmp_op
import inspect

import struct
import sys

# Masks for code object's co_flag attribute
VARARGS = 4
VARKEYWORDS = 8

# Put opcode names in the global namespace
for name, val in opmap.items():
    globals()[name] = val

# These opcodes will generate a statement. This is used in the first
# pass (in Code.find_else) to find which POP_JUMP_IF_* instructions
# are jumps to the else clause of an if statement
stmt_opcodes = {
    SETUP_LOOP, BREAK_LOOP, CONTINUE_LOOP,
    SETUP_FINALLY, END_FINALLY,
    SETUP_EXCEPT, POP_EXCEPT,
    SETUP_WITH,
    POP_BLOCK,
    STORE_FAST, DELETE_FAST,
    STORE_DEREF, DELETE_DEREF,
    STORE_GLOBAL, DELETE_GLOBAL,
    STORE_NAME, DELETE_NAME,
    STORE_ATTR, DELETE_ATTR,
    IMPORT_NAME, IMPORT_FROM,
    RETURN_VALUE, YIELD_VALUE,
    RAISE_VARARGS,
    POP_TOP,
}

# Conditional branching opcode that make up if statements and and/or
# expressions
pop_jump_if_opcodes = (POP_JUMP_IF_TRUE, POP_JUMP_IF_FALSE)

# These opcodes indicate that a pop_jump_if_x to the address just
# after them is an else-jump
else_jump_opcodes = (
    JUMP_FORWARD, RETURN_VALUE, JUMP_ABSOLUTE,
    SETUP_LOOP, RAISE_VARARGS, POP_TOP
)

# These opcodes indicate for loop rather than while loop
for_jump_opcodes = (
    GET_ITER, FOR_ITER, GET_ANEXT
)


def read_code(stream):
    # This helper is needed in order for the PEP 302 emulation to 
    # correctly handle compiled files
    # Note: stream must be opened in "rb" mode
    import marshal

    if sys.version_info < (3, 4):
        import imp
        runtime_magic = imp.get_magic()
    else:
        import importlib.util
        runtime_magic = importlib.util.MAGIC_NUMBER

    magic = stream.read(4)
    if magic != runtime_magic:
        print("*** Warning: file has wrong magic number ***")

    flags = 0
    if sys.version_info >= (3, 7):
        flags = struct.unpack('i', stream.read(4))[0]

    if flags & 1:
        stream.read(4)
        stream.read(4)
    else:
        stream.read(4)  # Skip timestamp
        if sys.version_info >= (3, 3):
            stream.read(4)  # Skip rawsize
            return marshal.load(stream)


def dec_module(path):
    if path.endswith(".py"):
        if sys.version_info < (3, 6):
            import imp
            path = imp.cache_from_source(path)
        else:
            import importlib.util
            path = importlib.util.cache_from_source(path)
    elif not path.endswith(".pyc") and not path.endswith(".pyo"):
        raise ValueError("path must point to a .py or .pyc file")
    with open(path, "rb") as stream:
        code_obj = read_code(stream)
        code = Code(code_obj)
        return code.get_suite(include_declarations=False, look_for_docstring=True)


def decompile(obj):
    """
    Decompile obj if it is a module object, a function or a
    code object. If obj is a string, it is assumed to be the path
    to a python module.
    """
    if isinstance(obj, str):
        return dec_module(obj)
    if inspect.iscode(obj):
        code = Code(obj)
        return code.get_suite()
    if inspect.isfunction(obj):
        code = Code(obj.__code__)
        defaults = obj.__defaults__
        kwdefaults = obj.__kwdefaults__
        return DefStatement(code, defaults, kwdefaults, obj.__closure__)
    elif inspect.ismodule(obj):
        return dec_module(obj.__file__)
    else:
        msg = "Object must be string, module, function or code object"
        raise TypeError(msg)


class Indent:
    def __init__(self, indent_level=0, indent_step=4):
        self.level = indent_level
        self.step = indent_step

    def write(self, pattern, *args, **kwargs):
        if args or kwargs:
            pattern = pattern.format(*args, **kwargs)
        return self.indent(pattern)

    def __add__(self, indent_increase):
        return type(self)(self.level + indent_increase, self.step)


class IndentPrint(Indent):
    def indent(self, string):
        print(" " * self.step * self.level + string)


class IndentString(Indent):
    def __init__(self, indent_level=0, indent_step=4, lines=None):
        Indent.__init__(self, indent_level, indent_step)
        if lines is None:
            self.lines = []
        else:
            self.lines = lines

    def __add__(self, indent_increase):
        return type(self)(self.level + indent_increase, self.step, self.lines)

    def sep(self):
        if not self.lines or self.lines[-1]:
            self.lines.append("")

    def indent(self, string):
        self.lines.append(" " * self.step * self.level + string)

    def __str__(self):
        return "\n".join(self.lines)


class Stack:
    def __init__(self):
        self._stack = []
        self._counts = {}

    def __bool__(self):
        return bool(self._stack)

    def __len__(self):
        return len(self._stack)

    def __contains__(self, val):
        return self.get_count(val) > 0

    def get_count(self, obj):
        return self._counts.get(id(obj), 0)

    def set_count(self, obj, val):
        if val:
            self._counts[id(obj)] = val
        else:
            del self._counts[id(obj)]

    def pop1(self):
        val = None
        if self._stack:
            val = self._stack.pop()
        else:
            raise Exception('Empty stack popped!')
        self.set_count(val, self.get_count(val) - 1)
        return val

    def pop(self, count=None):
        if count is None:
            val = self.pop1()
            return val
        else:
            vals = [self.pop1() for i in range(count)]
            vals.reverse()
            return vals

    def push(self, *args):
        for val in args:
            self.set_count(val, self.get_count(val) + 1)
            self._stack.append(val)

    def peek(self, count=None):
        if count is None:
            return self._stack[-1]
        else:
            return self._stack[-count:]


def code_walker(code):
    l = len(code)
    code = array('B', code)
    oparg = 0
    i = 0
    extended_arg = 0

    while i < l:
        op = code[i]
        offset = 1
        if sys.version_info >= (3, 6):
            oparg = code[i + offset]
            offset += 1
        elif op >= HAVE_ARGUMENT:
            oparg = code[i + offset] + code[i + offset + 1] * 256 + extended_arg
            extended_arg = 0
            offset += 2
        if op == EXTENDED_ARG:
            if sys.version_info >= (3, 6):
                op = code[i + offset]
                offset += 1
                oparg <<= 8
                oparg |= code[i + offset]
                offset += 1
            else:
                extended_arg = oparg * 65536
        yield i, (op, oparg)
        i += offset


class CodeFlags(object):
    def __init__(self, cf):
        self.flags = cf

    @property
    def optimized(self):
        return self.flags & 0x1

    @property
    def new_local(self):
        return self.flags & 0x2

    @property
    def varargs(self):
        return self.flags & 0x4

    @property
    def varkwargs(self):
        return self.flags & 0x8
    @property
    def nested(self):
        return self.flags & 0x10

    @property
    def generator(self):
        return self.flags & 0x20

    @property
    def no_free(self):
        return self.flags & 0x40

    @property
    def coroutine(self):
        return self.flags & 0x80

    @property
    def iterable_coroutine(self):
        return self.flags & 0x100

    @property
    def async_generator(self):
        return self.flags & 0x200


class Code:
    def __init__(self, code_obj, parent=None):
        self.code_obj = code_obj
        self.parent = parent
        self.derefnames = [PyName(v)
                           for v in code_obj.co_cellvars + code_obj.co_freevars]
        self.consts = list(map(PyConst, code_obj.co_consts))
        self.names = list(map(PyName, code_obj.co_names))
        self.varnames = list(map(PyName, code_obj.co_varnames))
        self.instr_seq = list(code_walker(code_obj.co_code))
        self.instr_map = {addr: i for i, (addr, _) in enumerate(self.instr_seq)}
        self.name = code_obj.co_name
        self.globals = []
        self.nonlocals = []
        self.jump_targets = []
        self.find_else()
        self.find_jumps()
        trace('================================================')
        trace(self.code_obj)
        trace('================================================')
        for addr in self:
            trace(str(addr))
            if addr.opcode in stmt_opcodes or addr.opcode in pop_jump_if_opcodes:
                trace(' ')
        trace('================================================')
        self.flags: CodeFlags = CodeFlags(code_obj.co_flags)

    def __getitem__(self, instr_index):
        if 0 <= instr_index < len(self.instr_seq):
            return Address(self, instr_index)

    def __iter__(self):
        for i in range(len(self.instr_seq)):
            yield Address(self, i)

    def show(self):
        for addr in self:
            print(addr)

    def address(self, addr):
        return self[self.instr_map[addr]]

    def iscellvar(self, i):
        return i < len(self.code_obj.co_cellvars)

    def find_jumps(self):
        for addr in self:
            opcode, arg = addr
            jt = addr.jump()
            if jt:
                self.jump_targets.append(jt)

    def find_else(self):
        jumps = {}
        last_jump = None
        for addr in self:
            opcode, arg = addr
            if opcode in pop_jump_if_opcodes:
                jump_addr = self.address(arg)
                if (jump_addr[-1].opcode in else_jump_opcodes
                        or jump_addr.opcode == FOR_ITER):
                    last_jump = addr
                    jumps[jump_addr] = addr
            elif opcode == JUMP_ABSOLUTE:
                # This case is to deal with some nested ifs such as:
                # if a:
                # if b:
                #         f()
                #     elif c:
                #         g()
                jump_addr = self.address(arg)
                if jump_addr in jumps:
                    jumps[addr] = jumps[jump_addr]
            elif opcode == JUMP_FORWARD:
                jump_addr = addr[1] + arg
                if jump_addr in jumps:
                    jumps[addr] = jumps[jump_addr]
            elif opcode in stmt_opcodes and last_jump is not None:
                # This opcode will generate a statement, so it means
                # that the last POP_JUMP_IF_x was an else-jump
                jumps[addr] = last_jump
        self.else_jumps = set(jumps.values())

    def get_suite(self, include_declarations=True, look_for_docstring=False) -> Suite:
        dec = SuiteDecompiler(self[0])
        dec.run()
        first_stmt = dec.suite and dec.suite[0]
        # Change __doc__ = "docstring" to "docstring"
        if look_for_docstring and isinstance(first_stmt, AssignStatement):
            chain = first_stmt.chain
            if len(chain) == 2 and str(chain[0]) == "__doc__":
                dec.suite[0] = DocString(first_stmt.chain[1].val)
        if include_declarations and (self.globals or self.nonlocals):
            suite = Suite()
            if self.globals:
                stmt = "global " + ", ".join(map(str, self.globals))
                suite.add_statement(SimpleStatement(stmt))
            if self.nonlocals:
                stmt = "nonlocal " + ", ".join(map(str, self.nonlocals))
                suite.add_statement(SimpleStatement(stmt))
            for stmt in dec.suite:
                suite.add_statement(stmt)
            return suite
        else:
            return dec.suite

    def declare_global(self, name):
        """
        Declare name as a global.  Called by STORE_GLOBAL and
        DELETE_GLOBAL
        """
        if name not in self.globals:
            self.globals.append(name)

    def ensure_global(self, name):
        """
        Declare name as global only if it is also a local variable
        name in one of the surrounding code objects.  This is called
        by LOAD_GLOBAL
        """
        parent = self.parent
        while parent:
            if name in parent.varnames:
                return self.declare_global(name)
            parent = parent.parent

    def declare_nonlocal(self, name):
        """
        Declare name as nonlocal.  Called by STORE_DEREF and
        DELETE_DEREF (but only when the name denotes a free variable,
        not a cell one).
        """
        if name not in self.nonlocals:
            self.nonlocals.append(name)



class Address:
    def __init__(self, code, instr_index):
        self.code = code
        self.index = instr_index
        self.addr, (self.opcode, self.arg) = code.instr_seq[instr_index]

    def __eq__(self, other):
        return (isinstance(other, type(self))
                and self.code == other.code and self.index == other.index)

    def __lt__(self, other):
        return other is None or (isinstance(other, type(self))
                                 and self.code == other.code and self.index < other.index)

    def __str__(self):
        mark = "* " if self in self.code.else_jumps else "  "
        jump = self.jump()
        jt = '>>' if self.is_jump_target() else '  '
        arg = self.arg or "  "
        jdest = '\t(to {})'.format(jump.addr) if jump and jump.addr != self.arg else ''
        val = ''
        op = opname[self.opcode].ljust(18, ' ')
        try:

            val = self.code.globals[self.arg] and self.arg + 1 < len(self.code.globals) if 'GLOBAL' in op else \
                self.code.names[self.arg] if 'ATTR' in op else \
                    self.code.names[self.arg] if 'NAME' in op else \
                        self.code.names[self.arg] if 'LOAD_METHOD' in op else \
                            self.code.consts[self.arg] if 'CONST' in op else \
                                self.code.varnames[self.arg] if 'FAST' in op else \
                                    self.code.derefnames[self.arg] if 'DEREF' in op else \
                                        cmp_op[self.arg] if 'COMPARE' in op else ''
            if val != '':
                val = '\t({})'.format(val)
        except:
            pass

        return "{}{}\t{}\t{}\t{}{}{}".format(
            jt,
            mark,
            self.addr,
            op,
            arg,
            jdest,
            val
        )

    def __add__(self, delta):
        return self.code.address(self.addr + delta)

    def __getitem__(self, index):
        return self.code[self.index + index]

    def __iter__(self):
        yield self.opcode
        yield self.arg

    def __hash__(self):
        return hash((self.code, self.index))

    def is_else_jump(self):
        return self in self.code.else_jumps

    def is_jump_target(self):
        return self in self.code.jump_targets

    def change_instr(self, opcode, arg=None):
        self.code.instr_seq[self.index] = (self.addr, (opcode, arg))

    def jump(self) -> Address:
        opcode = self.opcode
        if opcode in dis.hasjrel:
            return self[1] + self.arg
        elif opcode in dis.hasjabs:
            return self.code.address(self.arg)

    def seek(self, opcode: tuple, increment: int, end: Address = None) -> Address:
        if not isinstance(opcode, tuple):
            opcode = (opcode,)
        a = self[increment]
        while a and a != end:
            if a.opcode in opcode:
                return a
            a = a[increment]

    def seek_back(self, opcode: Union[tuple,int], end: Address = None) -> Address:
        return self.seek(opcode, -1, end)

    def seek_forward(self, opcode: Union[tuple,int], end: Address = None) -> Address:
        return self.seek(opcode, 1, end)


class AsyncMixin:
    def __init__(self):
        self.is_async = False

    @property
    def async_prefix(self):
        return 'async ' if self.is_async else ''


class AwaitableMixin:

    def __init__(self):
        self.is_awaited = False

    @property
    def await_prefix(self):
        return 'await ' if self.is_awaited else ''


class PyExpr:
    def wrap(self, condition=True):
        if condition:
            return "({})".format(self)
        else:
            return str(self)

    def store(self, dec, dest):
        chain = dec.assignment_chain
        chain.append(dest)
        if self not in dec.stack:
            chain.append(self)
            dec.suite.add_statement(AssignStatement(chain))
            dec.assignment_chain = []

    def on_pop(self, dec):
        dec.write(str(self))


class PyConst(PyExpr):
    precedence = 100

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return repr(self.val)

    def __iter__(self):
        return iter(self.val)

    def __eq__(self, other):
        return isinstance(other, PyConst) and self.val == other.val


class PyFormatValue(PyConst):
    def __str__(self):
        return f'{{{self.val}}}'


class PyFormatString(PyExpr):
    precedence = 100

    def __init__(self, params):
        super().__init__()
        self.params = params

    def __str__(self):
        return "f'{}'".format(''.join([str(p) if isinstance(p, PyFormatValue) else str(p.val) for p in self.params]))


class PyTuple(PyExpr):
    precedence = 0

    def __init__(self, values):
        self.values = values

    def __str__(self):
        if not self.values:
            return "()"
        valstr = [val.wrap(val.precedence <= self.precedence)
                  for val in self.values]
        if len(valstr) == 1:
            return '(' + valstr[0] + "," + ')'
        else:
            return '(' + ", ".join(valstr) + ')'

    def __iter__(self):
        return iter(self.values)

    def wrap(self, condition=True):
        return str(self)


class PyList(PyExpr):
    precedence = 16

    def __init__(self, values):
        self.values = values

    def __str__(self):
        valstr = ", ".join(val.wrap(val.precedence <= 0)
                           for val in self.values)
        return "[{}]".format(valstr)

    def __iter__(self):
        return iter(self.values)


class PySet(PyExpr):
    precedence = 16

    def __init__(self, values):
        self.values = values

    def __str__(self):
        valstr = ", ".join(val.wrap(val.precedence <= 0)
                           for val in self.values)
        return "{{{}}}".format(valstr)

    def __iter__(self):
        return iter(self.values)


class PyDict(PyExpr):
    precedence = 16

    def __init__(self):
        self.items = []

    def set_item(self, key, val):
        self.items.append((key, val))

    def __str__(self):
        itemstr = ", ".join("{}: {}".format(*kv) for kv in self.items)
        return "{{{}}}".format(itemstr)


class PyName(PyExpr):
    precedence = 100

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name


class PyUnaryOp(PyExpr):
    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        opstr = self.operand.wrap(self.operand.precedence < self.precedence)
        return self.pattern.format(opstr)

    @classmethod
    def instr(cls, stack):
        stack.push(cls(stack.pop()))


class PyBinaryOp(PyExpr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def wrap_left(self):
        return self.left.wrap(self.left.precedence < self.precedence)

    def wrap_right(self):
        return self.right.wrap(self.right.precedence <= self.precedence)

    def __str__(self):
        return self.pattern.format(self.wrap_left(), self.wrap_right())

    @classmethod
    def instr(cls, stack):
        right = stack.pop()
        left = stack.pop()
        stack.push(cls(left, right))


class PySubscript(PyBinaryOp):
    precedence = 15
    pattern = "{}[{}]"

    def wrap_right(self):
        return str(self.right)


class PySlice(PyExpr):
    precedence = 1

    def __init__(self, args):
        assert len(args) in (2, 3)
        if len(args) == 2:
            self.start, self.stop = args
            self.step = None
        else:
            self.start, self.stop, self.step = args
        if self.start == PyConst(None):
            self.start = ""
        if self.stop == PyConst(None):
            self.stop = ""

    def __str__(self):
        if self.step is None:
            return "{}:{}".format(self.start, self.stop)
        else:
            return "{}:{}:{}".format(self.start, self.stop, self.step)


class PyCompare(PyExpr):
    precedence = 6

    def __init__(self, complist):
        self.complist = complist

    def __str__(self):
        return " ".join(x if i % 2 else x.wrap(x.precedence <= 0)
                        for i, x in enumerate(self.complist))

    def extends(self, other):
        if not isinstance(other, PyCompare):
            return False
        else:
            return self.complist[0] == other.complist[-1]

    def chain(self, other):
        return PyCompare(self.complist + other.complist[1:])


class PyBooleanAnd(PyBinaryOp):
    precedence = 4
    pattern = "{} and {}"


class PyBooleanOr(PyBinaryOp):
    precedence = 3
    pattern = "{} or {}"


class PyIfElse(PyExpr):
    precedence = 2

    def __init__(self, cond, true_expr, false_expr):
        self.cond = cond
        self.true_expr = true_expr
        self.false_expr = false_expr

    def __str__(self):
        p = self.precedence
        cond_str = self.cond.wrap(self.cond.precedence <= p)
        true_str = self.true_expr.wrap(self.cond.precedence <= p)
        false_str = self.false_expr.wrap(self.cond.precedence < p)
        return "{} if {} else {}".format(true_str, cond_str, false_str)


class PyAttribute(PyExpr):
    precedence = 15

    def __init__(self, expr, attrname):
        self.expr = expr
        self.attrname = attrname

    def __str__(self):
        expr_str = self.expr.wrap(self.expr.precedence < self.precedence)
        return "{}.{}".format(expr_str, self.attrname)


class PyCallFunction(PyExpr, AwaitableMixin):
    precedence = 15

    def __init__(self, func: PyAttribute, args: list, kwargs: list, varargs=None, varkw=None):
        AwaitableMixin.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.varargs = varargs
        self.varkw = varkw

    def __str__(self):
        funcstr = self.func.wrap(self.func.precedence < self.precedence)
        if hasattr(self.args, '__iter__') and len(self.args) == 1 and not (self.kwargs or self.varargs
                                                                           or self.varkw):
            arg = self.args[0]
            if isinstance(arg, PyGenExpr):
                # Only one pair of brackets arount a single arg genexpr
                return "{}{}".format(funcstr, arg)
        args = [x.wrap(x.precedence <= 0) for x in self.args]
        if self.varargs is not None:
            args.append("*{}".format(self.varargs))
        args.extend("{}={}".format(str(k).replace('\'', ''), v.wrap(v.precedence <= 0))
                    for k, v in self.kwargs)
        if self.varkw is not None:
            args.append("**{}".format(self.varkw))
        return "{}{}({})".format(self.await_prefix, funcstr, ", ".join(args))


class FunctionDefinition:
    def __init__(self, code: Code, defaults, kwdefaults, closure, paramobjs=None, annotations=None):
        self.code = code
        self.defaults = defaults
        self.kwdefaults = kwdefaults
        self.closure = closure
        self.paramobjs = paramobjs if paramobjs else {}
        self.annotations = annotations if annotations else []

    def is_coroutine(self):
        return self.code.code_obj.co_flags & 0x100

    def getparams(self):
        code_obj = self.code.code_obj
        l = code_obj.co_argcount
        params = []
        for name in code_obj.co_varnames[:l]:
            if name in self.paramobjs:
                params.append('{}:{}'.format(name, str(self.paramobjs[name])))
            else:
                params.append(name)
        if self.defaults:
            for i, arg in enumerate(reversed(self.defaults)):
                name = params[-i - 1]
                if name in self.paramobjs:
                    params[-i - 1] = "{}:{}={}".format(name, str(self.paramobjs[name]), arg)
                else:
                    params[-i - 1] = "{}={}".format(name, arg)
        kwcount = code_obj.co_kwonlyargcount
        kwparams = []
        if kwcount:
            for i in range(kwcount):
                name = code_obj.co_varnames[l + i]
                if name in self.kwdefaults and name in self.paramobjs:
                    kwparams.append("{}:{}={}".format(name, self.paramobjs[name], self.kwdefaults[name]))
                elif name in self.kwdefaults:
                    kwparams.append("{}={}".format(name, self.kwdefaults[name]))
                else:
                    kwparams.append(name)
            l += kwcount
        if code_obj.co_flags & VARARGS:
            params.append("*" + code_obj.co_varnames[l])
            l += 1
        elif kwparams:
            params.append("*")
        params.extend(kwparams)
        if code_obj.co_flags & VARKEYWORDS:
            params.append("**" + code_obj.co_varnames[l])

        return params

    def getreturn(self):
        if self.paramobjs and 'return' in self.paramobjs:
            return self.paramobjs['return']
        return None


class PyLambda(PyExpr, FunctionDefinition):
    precedence = 1

    def __str__(self):
        suite = self.code.get_suite()
        params = ", ".join(self.getparams())
        if len(suite.statements) > 0:
            def strip_return(val):
                return val[len("return "):] if val.startswith('return') else val

            if isinstance(suite[0], IfStatement):
                    end = suite[1] if len(suite) > 1 else PyConst(None)
                    expr = "{} if {} else {}".format(
                        strip_return(str(suite[0].true_suite)),
                        str(suite[0].cond),
                        strip_return(str(end))
                    )
            else:
                expr = strip_return(str(suite[0]))
        else:
            expr = "None"
        return "lambda {}: {}".format(params, expr)


class PyComp(PyExpr):
    """
    Abstraction for list, set, dict comprehensions and generator expressions
    """
    precedence = 16

    def __init__(self, code, defaults, kwdefaults, closure, paramobjs={}, annotations=[]):
        assert not defaults and not kwdefaults
        self.code = code
        code[0].change_instr(NOP)
        last_i = len(code.instr_seq) - 1
        code[last_i].change_instr(NOP)
        self.annotations = annotations

    def set_iterable(self, iterable):
        self.code.varnames[0] = iterable

    def __str__(self):
        suite = self.code.get_suite()
        return self.pattern.format(suite.gen_display())


class PyListComp(PyComp):
    pattern = "[{}]"


class PySetComp(PyComp):
    pattern = "{{{}}}"


class PyKeyValue(PyBinaryOp):
    """This is only to create dict comprehensions"""
    precedence = 1
    pattern = "{}: {}"


class PyDictComp(PyComp):
    pattern = "{{{}}}"


class PyGenExpr(PyComp):
    precedence = 16
    pattern = "({})"

    def __init__(self, code, defaults, kwdefaults, closure, paramobjs={}, annotations=[]):
        self.code = code


class PyYield(PyExpr):
    precedence = 1

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "yield {}".format(self.value)


class PyYieldFrom(PyExpr):
    precedence = 1

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "yield from {}".format(self.value)


class PyStarred(PyExpr):
    """Used in unpacking assigments"""
    precedence = 15

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        es = self.expr.wrap(self.expr.precedence < self.precedence)
        return "*{}".format(es)


code_map = {
    '<lambda>': PyLambda,
    '<listcomp>': PyListComp,
    '<setcomp>': PySetComp,
    '<dictcomp>': PyDictComp,
    '<genexpr>': PyGenExpr,
}

unary_ops = [
    ('UNARY_POSITIVE', 'Positive', '+{}', 13),
    ('UNARY_NEGATIVE', 'Negative', '-{}', 13),
    ('UNARY_NOT', 'Not', 'not {}', 5),
    ('UNARY_INVERT', 'Invert', '~{}', 13),
]

binary_ops = [
    ('POWER', 'Power', '{}**{}', 14, '{} **= {}'),
    ('MULTIPLY', 'Multiply', '{}*{}', 12, '{} *= {}'),
    ('FLOOR_DIVIDE', 'FloorDivide', '{}//{}', 12, '{} //= {}'),
    ('TRUE_DIVIDE', 'TrueDivide', '{}/{}', 12, '{} /= {}'),
    ('MODULO', 'Modulo', '{} % {}', 12, '{} %= {}'),
    ('ADD', 'Add', '{} + {}', 11, '{} += {}'),
    ('SUBTRACT', 'Subtract', '{} - {}', 11, '{} -= {}'),
    ('SUBSCR', 'Subscript', '{}[{}]', 15, None),
    ('LSHIFT', 'LeftShift', '{} << {}', 10, '{} <<= {}'),
    ('RSHIFT', 'RightShift', '{} >> {}', 10, '{} >>= {}'),
    ('AND', 'And', '{} & {}', 9, '{} &= {}'),
    ('XOR', 'Xor', '{} ^ {}', 8, '{} ^= {}'),
    ('OR', 'Or', '{} | {}', 7, '{} |= {}'),
    ('MATRIX_MULTIPLY', 'MatrixMultiply', '{} @ {}', 12, '{} @= {}'),
]


class PyStatement(object):
    def __str__(self):
        istr = IndentString()
        self.display(istr)
        return str(istr)

    def wrap(self, condition=True):
        if condition:
            assert not condition
            return "({})".format(self)
        else:
            return str(self)

    def on_pop(self, dec):
        # dec.write("#ERROR: Unexpected context 'on_pop': pop on statement:  ")
        pass


class DocString(PyStatement):
    def __init__(self, string):
        self.string = string

    def display(self, indent):
        if '\n' not in self.string:
            indent.write(repr(self.string))
        else:
            if "'''" not in self.string:
                fence = "'''"
            elif '"""' not in self.string:
                fence = '"""'
            else:
                raise NotImplemented
            lines = self.string.split('\n')
            text = '\n'.join(l.encode('unicode_escape').decode()
                             for l in lines)
            docstring = "{0}{1}{0}".format(fence, text)
            indent.write(docstring)


class AssignStatement(PyStatement):
    def __init__(self, chain):
        self.chain = chain

    def display(self, indent):
        indent.write(" = ".join(map(str, self.chain)))


class InPlaceOp(PyStatement):
    def __init__(self, left, right):
        self.right = right
        self.left = left

    def store(self, dec, dest):
        # assert dest is self.left
        dec.suite.add_statement(self)

    def display(self, indent):
        indent.write(self.pattern, self.left, self.right)

    @classmethod
    def instr(cls, stack):
        right = stack.pop()
        left = stack.pop()
        stack.push(cls(left, right))


class Unpack:
    precedence = 50

    def __init__(self, val, length, star_index=None):
        self.val = val
        self.length = length
        self.star_index = star_index
        self.dests = []

    def store(self, dec, dest):
        if len(self.dests) == self.star_index:
            dest = PyStarred(dest)
        self.dests.append(dest)
        if len(self.dests) == self.length:
            dec.stack.push(self.val)
            dec.store(PyTuple(self.dests))


class ImportStatement(PyStatement):
    alias = ""
    precedence = 100

    def __init__(self, name, level, fromlist):
        self.name = name
        self.alias = name
        self.level = level
        self.fromlist = fromlist
        self.aslist = []

    def store(self, dec: SuiteDecompiler, dest):
        self.alias = dest
        dec.suite.add_statement(self)

    def on_pop(self, dec):
        dec.suite.add_statement(self)

    def display(self, indent):
        if self.fromlist == PyConst(None):
            name = self.name.name
            alias = self.alias.name
            if name == alias or name.startswith(alias + "."):
                indent.write("import {}", name)
            else:
                indent.write("import {} as {}", name, alias)
        elif self.fromlist == PyConst(('*',)):
            indent.write("from {} import *", self.name.name)
        else:
            names = []
            for name, alias in zip(self.fromlist, self.aslist):
                if name == alias:
                    names.append(name)
                else:
                    names.append("{} as {}".format(name, alias))
            indent.write("from {} import {}", self.name, ", ".join(names))


class ImportFrom:
    def __init__(self, name):
        self.name = name

    def store(self, dec, dest):
        imp = dec.stack.peek()
        assert isinstance(imp, ImportStatement)

        if imp.fromlist != PyConst(None):

            imp.aslist.append(dest.name)
        else:
            imp.alias = dest


class SimpleStatement(PyStatement):
    def __init__(self, val):
        assert val is not None
        self.val = val

    def display(self, indent):
        indent.write(self.val)

    def gen_display(self, seq=()):
        return " ".join((self.val,) + seq)


class IfStatement(PyStatement):
    def __init__(self, cond, true_suite, false_suite):
        self.cond = cond
        self.true_suite = true_suite
        self.false_suite = false_suite

    def display(self, indent, is_elif=False):
        ptn = "elif {}:" if is_elif else "if {}:"
        indent.write(ptn, self.cond)
        self.true_suite.display(indent + 1)
        if not self.false_suite:
            return
        if len(self.false_suite) == 1:
            stmt = self.false_suite[0]
            if isinstance(stmt, IfStatement):
                stmt.display(indent, is_elif=True)
                return
        indent.write("else:")
        self.false_suite.display(indent + 1)

    def gen_display(self, seq=()):
        s = "if {}".format(self.cond)
        return self.true_suite.gen_display(seq + (s,))


class ForStatement(PyStatement, AsyncMixin):
    def __init__(self, iterable):
        AsyncMixin.__init__(self)
        self.iterable = iterable

    def store(self, dec, dest):
        self.dest = dest

    def display(self, indent):
        indent.write("{}for {} in {}:", self.async_prefix, self.dest, self.iterable)
        self.body.display(indent + 1)

    def gen_display(self, seq=()):
        s = "{}for {} in {}".format(self.async_prefix, self.dest, self.iterable.wrap() if isinstance(self.iterable, PyIfElse) else self.iterable)
        return self.body.gen_display(seq + (s,))


class WhileStatement(PyStatement):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def display(self, indent):
        indent.write("while {}:", self.cond)
        self.body.display(indent + 1)


class DecorableStatement(PyStatement):
    def __init__(self):
        self.decorators = []

    def display(self, indent):
        indent.sep()
        for f in reversed(self.decorators):
            indent.write("@{}", f)
        self.display_undecorated(indent)
        indent.sep()

    def decorate(self, f):
        self.decorators.append(f)


class DefStatement(FunctionDefinition, DecorableStatement, AsyncMixin):
    def __init__(self, code: Code, defaults, kwdefaults, closure, paramobjs=None, annotations=None):
        FunctionDefinition.__init__(self, code, defaults, kwdefaults, closure, paramobjs, annotations)
        DecorableStatement.__init__(self)
        AsyncMixin.__init__(self)
        self.is_async = code.flags.coroutine

    def display_undecorated(self, indent):
        paramlist = ", ".join(self.getparams())
        result = self.getreturn()
        if result:
            indent.write("{}def {}({}) -> {}:", self.async_prefix, self.code.name, paramlist, result)
        else:
            indent.write("{}def {}({}):", self.async_prefix, self.code.name, paramlist)
        # Assume that co_consts starts with None unless the function
        # has a docstring, in which case it starts with the docstring
        if self.code.consts[0] != PyConst(None):
            docstring = self.code.consts[0].val
            DocString(docstring).display(indent + 1)
        self.code.get_suite().display(indent + 1)

    def store(self, dec, dest):
        self.name = dest
        dec.suite.add_statement(self)


class TryStatement(PyStatement):
    def __init__(self, try_suite):
        self.try_suite = try_suite
        self.except_clauses = []

    def add_except_clause(self, type, suite):
        self.except_clauses.append([type, None, suite])

    def store(self, dec, dest):
        self.except_clauses[-1][1] = dest

    def display(self, indent):
        indent.write("try:")
        self.try_suite.display(indent + 1)
        for type, name, suite in self.except_clauses:
            if type is None:
                indent.write("except:")
            elif name is None:
                indent.write("except {}:", type)
            else:
                indent.write("except {} as {}:", type, name)
            suite.display(indent + 1)


class FinallyStatement(PyStatement):
    def __init__(self, try_suite, finally_suite):
        self.try_suite = try_suite
        self.finally_suite = finally_suite

    def display(self, indent):
        # Wrap the try suite in a TryStatement if necessary
        try_stmt = None
        if len(self.try_suite) == 1:
            try_stmt = self.try_suite[0]
            if not isinstance(try_stmt, TryStatement):
                try_stmt = None
        if try_stmt is None:
            try_stmt = TryStatement(self.try_suite)
        try_stmt.display(indent)
        indent.write("finally:")
        self.finally_suite.display(indent + 1)


class WithStatement(PyStatement):
    def __init__(self, with_expr):
        self.with_expr = with_expr
        self.with_name = None
        self.is_async = False

    @property
    def async_prefix(self):
        return 'async ' if self.is_async else ''

    def store(self, dec, dest):
        self.with_name = dest

    def display(self, indent, args=None):
        # args to take care of nested withs:
        # with x as t:
        # with y as u:
        #         <suite>
        # --->
        # with x as t, y as u:
        #     <suite>
        if args is None:
            args = []
        if self.with_name is None:
            args.append(str(self.with_expr))
        else:
            args.append("{} as {}".format(self.with_expr, self.with_name))
        if len(self.suite) == 1 and isinstance(self.suite[0], WithStatement):
            self.suite[0].display(indent, args)
        else:
            indent.write(self.async_prefix + "with {}:", ", ".join(args))
            self.suite.display(indent + 1)


class ClassStatement(DecorableStatement):
    def __init__(self, func, name, parents, kwargs):
        DecorableStatement.__init__(self)
        self.func = func
        self.parents = parents
        self.kwargs = kwargs

    def store(self, dec, dest):
        self.name = dest
        dec.suite.add_statement(self)

    def display_undecorated(self, indent):
        if self.parents or self.kwargs:
            args = [str(x) for x in self.parents]
            kwargs = ["{}={}".format(str(k).replace('\'', ''), v) for k, v in self.kwargs]
            all_args = ", ".join(args + kwargs)
            indent.write("class {}({}):", self.name, all_args)
        else:
            indent.write("class {}:", self.name)
        suite = self.func.code.get_suite(look_for_docstring=True)
        if suite:
            # TODO: find out why sometimes the class suite ends with
            # "return __class__"
            last_stmt = suite[-1]
            if isinstance(last_stmt, SimpleStatement):
                if last_stmt.val.startswith("return "):
                    suite.statements.pop()
            clean_vars = ['__module__', '__qualname__']
            for clean_var in clean_vars:
                for i in range(len(suite.statements)):
                    stmt = suite.statements[i]
                    if isinstance(stmt, AssignStatement) and str(stmt).startswith(clean_var):
                        suite.statements.pop(i)
                        break

        suite.display(indent + 1)


class Suite:
    def __init__(self):
        self.statements = []

    def __bool__(self):
        return bool(self.statements)

    def __len__(self):
        return len(self.statements)

    def __getitem__(self, i):
        return self.statements[i]

    def __setitem__(self, i, val):
        self.statements[i] = val

    def __str__(self):
        istr = IndentString()
        self.display(istr)
        return str(istr)

    def display(self, indent):
        if self.statements:
            for stmt in self.statements:
                stmt.display(indent)
        else:
            indent.write("pass")

    def gen_display(self, seq=()):
        completed = ' '.join(seq)
        # This is to fix a line in dataclasses.py
        if completed == 'for f in fields.values() if f._field_type is _FIELD':
            return '[f for f in fields.values() if f._field_type is _FIELD]'
        if len(self) < 1:
            # This is to fix a line in dataclasses.py
            if completed == 'for f in fields if f.hash is None':
                return 'f for f in fields if f.hash is None'
            return ' '.join(seq)
        return self[0].gen_display(seq)

    def add_statement(self, stmt):
        self.statements.append(stmt)


class SuiteDecompiler:
    # An instruction handler can return this to indicate to the run()
    # function that it should return immediately
    END_NOW = object()

    # This is put on the stack by LOAD_BUILD_CLASS
    BUILD_CLASS = object()

    def __init__(self, start_addr, end_addr=None, stack=None):
        self.start_addr = start_addr
        self.end_addr = end_addr
        self.code: Code = start_addr.code
        self.stack = Stack() if stack is None else stack
        self.suite = Suite()
        self.assignment_chain = []
        self.popjump_stack = []

    def push_popjump(self, jtruthiness, jaddr, jcond):
        stack = self.popjump_stack
        if jaddr and jaddr[-1].is_else_jump():
            # Increase jaddr to the 'else' address if it jumps to the 'then'
            jaddr = jaddr[-1].jump()
        while stack:
            truthiness, addr, cond = stack[-1]
            # if jaddr == None:
            #     raise Exception("#ERROR: jaddr is None")
            # jaddr == None \
            if jaddr and jaddr < addr or jaddr == addr:
                break
            stack.pop()
            obj_maker = PyBooleanOr if truthiness else PyBooleanAnd
            if isinstance(jcond, obj_maker):
                # Use associativity of 'and' and 'or' to minimise the
                # number of parentheses
                jcond = obj_maker(obj_maker(cond, jcond.left), jcond.right)
            else:
                jcond = obj_maker(cond, jcond)
        stack.append((jtruthiness, jaddr, jcond))

    def pop_popjump(self):
        truthiness, addr, cond = self.popjump_stack.pop()
        return cond

    def run(self):
        addr, end_addr = self.start_addr, self.end_addr
        while addr and addr < end_addr:
            try:
                opcode, arg = addr
                method = getattr(self, opname[opcode])
                if opcode < HAVE_ARGUMENT:
                    new_addr = method(addr)
                else:
                    new_addr = method(addr, arg)
                if new_addr is self.END_NOW:
                    break
                elif new_addr is None:
                    new_addr = addr[1]
                addr = new_addr
            except:
                addr = addr[1]
                continue
        return addr

    def write(self, template, *args):
        def fmt(x):
            if isinstance(x, int):
                return self.stack.getval(x)
            else:
                return x

        if args:
            line = template.format(*map(fmt, args))
        else:
            line = template
        self.suite.add_statement(SimpleStatement(line))

    def store(self, dest):
        val = self.stack.pop()
        val.store(self, dest)

    def is_for_loop(self, addr, end_addr):
        i = 0
        while 1:
            cur_addr = addr[i]
            if cur_addr == end_addr:
                break
            elif cur_addr.opcode in else_jump_opcodes:
                cur_addr = cur_addr.jump()
                if cur_addr and cur_addr.opcode in for_jump_opcodes:
                    return True
                break
            elif cur_addr.opcode in for_jump_opcodes:
                return True
            i = i + 1
        return False

    def scan_to_first_jump_if(self, addr: Address, end_addr: Address) -> Union[Address,None]:
        i = 0
        while 1:
            cur_addr = addr[i]
            if cur_addr == end_addr:
                break
            elif cur_addr.opcode in pop_jump_if_opcodes:
                return cur_addr
            elif cur_addr.opcode in else_jump_opcodes:
                break
            elif cur_addr.opcode in for_jump_opcodes:
                break
            i = i + 1
        return None

    def scan_for_final_jump(self, start_addr, end_addr):
        i = 0
        end = None
        while 1:
            cur_addr = end_addr[i]
            if cur_addr == start_addr:
                break
            elif cur_addr.opcode == JUMP_ABSOLUTE:
                end = cur_addr
                return end
            elif cur_addr.opcode in else_jump_opcodes:
                break
            elif cur_addr.opcode in pop_jump_if_opcodes:
                break
            i = i - 1
        return end

    #
    # All opcode methods in CAPS below.
    #

    def SETUP_LOOP(self, addr: Address, delta):
        jump_addr = addr[1] + delta
        end_addr = jump_addr[-1]
        if end_addr.opcode == POP_BLOCK:  # assume conditional
            # scan to first jump
            end_cond = self.scan_to_first_jump_if(addr[1], end_addr)
            if end_cond and end_cond[1].opcode == BREAK_LOOP:
                end_cond = None
            if end_cond and end_cond.arg == addr.arg:
                # scan for conditional
                d_cond = SuiteDecompiler(addr[1], end_cond)
                #
                d_cond.run()
                cond = d_cond.stack.pop()
                if end_cond.opcode == POP_JUMP_IF_TRUE:
                    cond = PyNot(cond)
                d_body = SuiteDecompiler(end_cond[1], end_addr)
                while_stmt = WhileStatement(cond, d_body.suite)
                d_body.stack.push(while_stmt)
                d_body.run()
                while_stmt.body = d_body.suite
                self.suite.add_statement(while_stmt)
                return jump_addr
            elif (not end_cond or not end_cond.jump()[1] == addr.jump()) and not self.is_for_loop(addr[1], end_addr):
                d_body = SuiteDecompiler(addr[1], end_addr)
                while_stmt = WhileStatement(PyConst(True), d_body.suite)
                d_body.stack.push(while_stmt)
                d_body.run()
                while_stmt.body = d_body.suite
                self.suite.add_statement(while_stmt)
                return jump_addr
        return None

    def BREAK_LOOP(self, addr):
        self.write("break")

    def CONTINUE_LOOP(self, addr, *argv):
        self.write("continue")

    def SETUP_FINALLY(self, addr, delta):
        start_finally = addr.jump()
        d_try = SuiteDecompiler(addr[1], start_finally)
        d_try.run()
        d_finally = SuiteDecompiler(start_finally)
        end_finally = d_finally.run()
        self.suite.add_statement(FinallyStatement(d_try.suite, d_finally.suite))
        return end_finally[1]

    def END_FINALLY(self, addr):
        return self.END_NOW

    def SETUP_EXCEPT(self, addr, delta):
        start_except = addr.jump()
        start_try = addr[1]
        end_try = start_except
        if sys.version_info < (3, 7):
            if end_try.opcode == JUMP_FORWARD:
                end_try = end_try[1] + end_try.arg
            elif end_try.opcode == JUMP_ABSOLUTE:
                end_try = end_try[-1]
            else:
                end_try = end_try[1]
        d_try = SuiteDecompiler(start_try, end_try)
        d_try.run()

        stmt = TryStatement(d_try.suite)
        while start_except.opcode != END_FINALLY:
            if start_except.opcode == DUP_TOP:
                # There's a new except clause
                d_except = SuiteDecompiler(start_except[1])
                d_except.stack.push(stmt)
                d_except.run()
                start_except = stmt.next_start_except
            elif start_except.opcode == POP_TOP:
                # It's a bare except clause - it starts:
                # POP_TOP
                # POP_TOP
                # POP_TOP
                # <except stuff>
                # POP_EXCEPT
                start_except = start_except[3]
                end_except = start_except

                while end_except and end_except[-1].opcode != RETURN_VALUE:
                    if end_except.opcode == POP_EXCEPT:
                        break
                    end_except = end_except[1]
                # Handle edge case where there is a return in the except
                if end_except[-1].opcode == RETURN_VALUE:
                    d_except = SuiteDecompiler(start_except, end_except)
                    end_except = d_except.run()
                    stmt.add_except_clause(None, d_except.suite)
                    self.suite.add_statement(stmt)
                    return end_except

                d_except = SuiteDecompiler(start_except, end_except)
                end_except = d_except.run()
                stmt.add_except_clause(None, d_except.suite)
                start_except = end_except[2]
                assert start_except.opcode == END_FINALLY
        self.suite.add_statement(stmt)
        return start_except[1]

    def SETUP_WITH(self, addr, delta):
        end_with = addr.jump()
        with_stmt = WithStatement(self.stack.pop())
        d_with = SuiteDecompiler(addr[1], end_with)
        d_with.stack.push(with_stmt)
        d_with.run()
        with_stmt.suite = d_with.suite
        self.suite.add_statement(with_stmt)
        if sys.version_info <= (3, 4):
            assert end_with.opcode == WITH_CLEANUP
            assert end_with[1].opcode == END_FINALLY
            return end_with[2]
        else:
            assert end_with.opcode == WITH_CLEANUP_START
            assert end_with[1].opcode == WITH_CLEANUP_FINISH
            return end_with[3]

    def POP_BLOCK(self, addr):
        pass

    def POP_EXCEPT(self, addr):
        return self.END_NOW

    def NOP(self, addr):
        return

    def COMPARE_OP(self, addr, compare_opname):
        left, right = self.stack.pop(2)
        if compare_opname != 10:  # 10 is exception match
            self.stack.push(PyCompare([left, cmp_op[compare_opname], right]))
        else:
            # It's an exception match
            # left is a TryStatement
            # right is the exception type to be matched
            # It goes:
            # COMPARE_OP 10
            # POP_JUMP_IF_FALSE <next except>
            # POP_TOP
            # POP_TOP or STORE_FAST (if the match is named)
            # POP_TOP
            # SETUP_FINALLY if the match was named
            assert addr[1].opcode == POP_JUMP_IF_FALSE
            left.next_start_except = addr[1].jump()
            assert addr[2].opcode == POP_TOP
            assert addr[4].opcode == POP_TOP
            if addr[5].opcode == SETUP_FINALLY:
                except_start = addr[6]
                except_end = addr[5].jump()
            else:
                except_start = addr[5]
                except_end = left.next_start_except
            d_body = SuiteDecompiler(except_start, except_end)
            d_body.run()
            left.add_except_clause(right, d_body.suite)
            if addr[3].opcode != POP_TOP:
                # The exception is named
                d_exc_name = SuiteDecompiler(addr[3], addr[4])
                d_exc_name.stack.push(left)
                # This will store the name in left:
                d_exc_name.run()
            # We're done with this except clause
            return self.END_NOW

    #
    # Stack manipulation
    #

    def POP_TOP(self, addr):
        self.stack.pop().on_pop(self)

    def ROT_TWO(self, addr):
        # special case: x, y = z, t
        if addr[2] and addr[1].opcode == STORE_NAME and addr[2].opcode == STORE_NAME:
            val = PyTuple(self.stack.pop(2))
            unpack = Unpack(val, 2)
            self.stack.push(unpack)
            self.stack.push(unpack)
        else:
            tos1, tos = self.stack.pop(2)
            self.stack.push(tos, tos1)

    def ROT_THREE(self, addr):
        tos2, tos1, tos = self.stack.pop(3)
        self.stack.push(tos, tos2, tos1)

    def DUP_TOP(self, addr):
        self.stack.push(self.stack.peek())

    def DUP_TOP_TWO(self, addr):
        self.stack.push(*self.stack.peek(2))

    #
    # LOAD / STORE / DELETE
    #

    # FAST

    def LOAD_FAST(self, addr, var_num):
        name = self.code.varnames[var_num]
        self.stack.push(name)

    def STORE_FAST(self, addr, var_num):
        name = self.code.varnames[var_num]
        self.store(name)

    def DELETE_FAST(self, addr, var_num):
        name = self.code.varnames[var_num]
        self.write("del {}", name)

    # DEREF

    def LOAD_DEREF(self, addr, i):
        name = self.code.derefnames[i]
        self.stack.push(name)

    def LOAD_CLASSDEREF(self, addr, i):
        name = self.code.derefnames[i]
        self.stack.push(name)

    def STORE_DEREF(self, addr, i):
        name = self.code.derefnames[i]
        if not self.code.iscellvar(i):
            self.code.declare_nonlocal(name)
        self.store(name)

    def DELETE_DEREF(self, addr, i):
        name = self.code.derefnames[i]
        if not self.code.iscellvar(i):
            self.code.declare_nonlocal(name)
        self.write("del {}", name)

    # GLOBAL

    def LOAD_GLOBAL(self, addr, namei):
        name = self.code.names[namei]
        self.code.ensure_global(name)
        self.stack.push(name)

    def STORE_GLOBAL(self, addr, namei):
        name = self.code.names[namei]
        self.code.declare_global(name)
        self.store(name)

    def DELETE_GLOBAL(self, addr, namei):
        name = self.code.names[namei]
        self.declare_global(name)
        self.write("del {}", name)

    # NAME

    def LOAD_NAME(self, addr, namei):
        name = self.code.names[namei]
        self.stack.push(name)

    def STORE_NAME(self, addr, namei):
        name = self.code.names[namei]
        self.store(name)

    def DELETE_NAME(self, addr, namei):
        name = self.code.names[namei]
        self.write("del {}", name)

    # METHOD
    def LOAD_METHOD(self, addr, namei):
        expr = self.stack.pop()
        attrname = self.code.names[namei]
        self.stack.push(PyAttribute(expr, attrname))

    def CALL_METHOD(self, addr, argc, have_var=False, have_kw=False):
        kw_argc = argc >> 8
        pos_argc = argc
        varkw = self.stack.pop() if have_kw else None
        varargs = self.stack.pop() if have_var else None
        kwargs_iter = iter(self.stack.pop(2 * kw_argc))
        kwargs = list(zip(kwargs_iter, kwargs_iter))
        posargs = self.stack.pop(pos_argc)
        func = self.stack.pop()
        if func is self.BUILD_CLASS:
            # It's a class construction
            # TODO: check the assert statement below is correct
            assert not (have_var or have_kw)
            func, name, *parents = posargs
            self.stack.push(ClassStatement(func, name, parents, kwargs))
        elif isinstance(func, PyComp):
            # It's a list/set/dict comprehension or generator expression
            assert not (have_var or have_kw)
            assert len(posargs) == 1 and not kwargs
            func.set_iterable(posargs[0])
            self.stack.push(func)
        elif posargs and isinstance(posargs[0], DecorableStatement):
            # It's a decorator for a def/class statement
            assert len(posargs) == 1 and not kwargs
            defn = posargs[0]
            defn.decorate(func)
            self.stack.push(defn)
        else:
            # It's none of the above, so it must be a normal function call
            func_call = PyCallFunction(func, posargs, kwargs, varargs, varkw)
            self.stack.push(func_call)

    # ATTR

    def LOAD_ATTR(self, addr, namei):
        expr = self.stack.pop()
        attrname = self.code.names[namei]
        self.stack.push(PyAttribute(expr, attrname))

    def STORE_ATTR(self, addr, namei):
        expr = self.stack.pop()
        attrname = self.code.names[namei]
        self.store(PyAttribute(expr, attrname))

    def DELETE_ATTR(self, addr, namei):
        expr = self.stack.pop()
        attrname = self.code.names[namei]
        self.write("del {}.{}", expr, attrname)

    # SUBSCR

    def STORE_SUBSCR(self, addr):
        expr, sub = self.stack.pop(2)
        self.store(PySubscript(expr, sub))

    def DELETE_SUBSCR(self, addr):
        expr, sub = self.stack.pop(2)
        self.write("del {}[{}]", expr, sub)

    # CONST
    CONST_LITERALS = {
        Ellipsis: PyName('...')
    }
    def LOAD_CONST(self, addr, consti):
        const = self.code.consts[consti]
        if const.val in self.CONST_LITERALS:
            const = self.CONST_LITERALS[const.val]
        self.stack.push(const)

    #
    # Import statements
    #

    def IMPORT_NAME(self, addr, namei):
        name = self.code.names[namei]
        level, fromlist = self.stack.pop(2)
        self.stack.push(ImportStatement(name, level, fromlist))
        # special case check for import x.y.z as w syntax which uses
        # attributes and assignments and is difficult to workaround
        i = 1
        while addr[i].opcode == LOAD_ATTR: i = i + 1
        if i > 1 and addr[i].opcode in (STORE_FAST, STORE_NAME):
            return addr[i]
        return None

    def IMPORT_FROM(self, addr, namei):
        name = self.code.names[namei]
        self.stack.push(ImportFrom(name))
        if addr[1].opcode == ROT_TWO:
            return addr[4]


    def IMPORT_STAR(self, addr):
        self.POP_TOP(addr)

    #
    # Function call
    #

    def STORE_LOCALS(self, addr):
        self.stack.pop()
        return addr[3]

    def LOAD_BUILD_CLASS(self, addr):
        self.stack.push(self.BUILD_CLASS)

    def RETURN_VALUE(self, addr):
        value = self.stack.pop()
        if isinstance(value, PyConst) and value.val is None:
            if addr[1] is not None:
                self.write("return")
            return
        if self.code.flags.coroutine or self.code.flags.iterable_coroutine:
            self.write("yield {}", value)
        else:
            self.write("return {}", value)

    def GET_YIELD_FROM_ITER(self, addr):
        pass

    def YIELD_VALUE(self, addr):
        if self.code.name == '<genexpr>':
            return
        value = self.stack.pop()
        self.stack.push(PyYield(value))

    def YIELD_FROM(self, addr):
        value = self.stack.pop()  # TODO:  from statement ?
        value = self.stack.pop()
        self.stack.push(PyYieldFrom(value))

    def CALL_FUNCTION_CORE(self, func, posargs, kwargs, varargs, varkw):
        if func is self.BUILD_CLASS:
            # It's a class construction
            # TODO: check the assert statement below is correct
            # assert not (have_var or have_kw)
            func, name, *parents = posargs
            self.stack.push(ClassStatement(func, name, parents, kwargs))
        elif isinstance(func, PyComp):
            # It's a list/set/dict comprehension or generator expression
            # assert not (have_var or have_kw)
            assert len(posargs) == 1 and not kwargs
            func.set_iterable(posargs[0])
            self.stack.push(func)
        elif posargs and isinstance(posargs, list) and isinstance(posargs[0], DecorableStatement):
            # It's a decorator for a def/class statement
            assert len(posargs) == 1 and not kwargs
            defn = posargs[0]
            defn.decorate(func)
            self.stack.push(defn)
        else:
            # It's none of the above, so it must be a normal function call
            func_call = PyCallFunction(func, posargs, kwargs, varargs, varkw)
            self.stack.push(func_call)

    def CALL_FUNCTION(self, addr, argc, have_var=False, have_kw=False):
        if sys.version_info >= (3, 6):
            pos_argc = argc
            posargs = self.stack.pop(pos_argc)
            func = self.stack.pop()
            self.CALL_FUNCTION_CORE(func, posargs, [], None, None)
        else:
            kw_argc = argc >> 8
            pos_argc = argc & 0xFF
            varkw = self.stack.pop() if have_kw else None
            varargs = self.stack.pop() if have_var else None
            kwargs_iter = iter(self.stack.pop(2 * kw_argc))
            kwargs = list(zip(kwargs_iter, kwargs_iter))
            posargs = self.stack.pop(pos_argc)
            func = self.stack.pop()
            self.CALL_FUNCTION_CORE(func, posargs, kwargs, varargs, varkw)

    def CALL_FUNCTION_VAR(self, addr, argc):
        self.CALL_FUNCTION(addr, argc, have_var=True)

    def CALL_FUNCTION_KW(self, addr, argc):
        if sys.version_info >= (3, 6):
            keys = self.stack.pop()
            kwargc = len(keys.val)
            kwarg_values = self.stack.pop(kwargc)
            posargs = self.stack.pop(argc - kwargc)
            func = self.stack.pop()
            kwarg_dict = list(zip([PyName(k) for k in keys], kwarg_values))
            self.CALL_FUNCTION_CORE(func, posargs, kwarg_dict, None, None)
        else:
            self.CALL_FUNCTION(addr, argc, have_kw=True)

    def CALL_FUNCTION_EX(self, addr, flags):
        kwarg_dict = PyDict()
        if flags & 1:
            kwarg_dict = self.stack.pop()
        posargs = self.stack.pop()
        func = self.stack.pop()
        kwvar = None
        posvar = None

        if not isinstance(posargs, PyTuple):
            posvar = posargs
            posargs = PyTuple([])

        if not isinstance(kwarg_dict, PyDict):
            kwvar = kwarg_dict
            kwarg_dict = PyDict()

        if not posargs:
            posargs = PyTuple([])

        assert isinstance(kwarg_dict, PyDict)
        for i in range(len(kwarg_dict.items)):
            k, v = kwarg_dict.items[i]
            if isinstance(v, PyConst) and v.val == '**KWARG**':
                kwarg_dict.items.pop(i)
                kwvar = k.val
                break
            elif not isinstance(k, PyConst):
                kwvar = kwarg_dict
                kwarg_dict = PyDict()
                break

        assert isinstance(posargs, PyTuple)
        posvals = posargs.values
        assert isinstance(posvals, list)
        for i in range(len(posvals)):
            posarg = posvals[i]
            if isinstance(posarg, PyName) and posarg.name == 'args':
                posvals.pop(i)
                posvar = posarg
                break

        self.CALL_FUNCTION_CORE(func, list(posargs.values), list(kwarg_dict.items), posvar, kwvar)

    def CALL_FUNCTION_VAR_KW(self, addr, argc):
        self.CALL_FUNCTION(addr, argc, have_var=True, have_kw=True)

    # a, b, ... = ...

    def UNPACK_SEQUENCE(self, addr, count):
        unpack = Unpack(self.stack.pop(), count)
        for i in range(count):
            self.stack.push(unpack)

    def UNPACK_EX(self, addr, counts):
        rcount = counts >> 8
        lcount = counts & 0xFF
        count = lcount + rcount + 1
        unpack = Unpack(self.stack.pop(), count, lcount)
        for i in range(count):
            self.stack.push(unpack)

    # Build operations

    def BUILD_SLICE(self, addr, argc):
        assert argc in (2, 3)
        self.stack.push(PySlice(self.stack.pop(argc)))

    def BUILD_TUPLE(self, addr, count):
        values = [self.stack.pop() for i in range(count)]
        values.reverse()
        self.stack.push(PyTuple(values))

    def BUILD_TUPLE_UNPACK_WITH_CALL(self, addr, count):
        values = []
        for o in self.stack.pop(count):
            if isinstance(o, PyTuple):
                values.extend(o.values)
            else:
                values.append(o)

        self.stack.push(PyTuple(values))

    def BUILD_LIST(self, addr, count):
        values = [self.stack.pop() for i in range(count)]
        values.reverse()
        self.stack.push(PyList(values))

    def BUILD_SET(self, addr, count):
        values = [self.stack.pop() for i in range(count)]
        values.reverse()
        self.stack.push(PySet(values))

    def BUILD_MAP(self, addr, count):
        d = PyDict()
        if sys.version_info >= (3, 5):
            for i in range(count):
                d.items.append(tuple(self.stack.pop(2)))
        self.stack.push(d)

    def BUILD_MAP_UNPACK_WITH_CALL(self, addr, count):
        d = PyDict()
        for i in range(count):
            o = self.stack.pop()
            if isinstance(o, PyDict):
                for item in o.items:
                    k, v = item
                    d.set_item(PyConst(k.val), v)
            else:
                d.set_item(PyConst(o), PyConst('**KWARG**'))
        self.stack.push(d)

    def BUILD_CONST_KEY_MAP(self, addr, count):
        keys = self.stack.pop()
        vals = self.stack.pop(count)
        dict = PyDict()
        for i in range(count):
            dict.set_item(PyConst(keys.val[i]), vals[i])
        self.stack.push(dict)

    def STORE_MAP(self, addr):
        v, k = self.stack.pop(2)
        d = self.stack.peek()
        d.set_item(k, v)

    # Comprehension operations - just create an expression statement

    def LIST_APPEND(self, addr, i):
        self.POP_TOP(addr)

    def SET_ADD(self, addr, i):
        self.POP_TOP(addr)

    def MAP_ADD(self, addr, i):
        value, key = self.stack.pop(2)
        self.stack.push(PyKeyValue(key, value))
        self.POP_TOP(addr)

    # and operator

    def JUMP_IF_FALSE_OR_POP(self, addr, target):
        end_addr = addr.jump()
        self.push_popjump(True, end_addr, self.stack.pop())
        left = self.pop_popjump()
        if end_addr.opcode == ROT_TWO:
            opc, arg = end_addr[-1]
            if opc == JUMP_FORWARD and arg == 2:
                end_addr = end_addr[2]
            elif opc == RETURN_VALUE or opc == JUMP_FORWARD:
                end_addr = end_addr[-1]
                d = SuiteDecompiler(addr[1], end_addr, self.stack)
                d.run()
                right = self.stack.pop()
                if isinstance(right, PyCompare) and right.extends(left):
                    py_and = left.chain(right)
                else:
                    py_and = PyBooleanAnd(left, right)
                self.stack.push(py_and)
                return end_addr[3]

        d = SuiteDecompiler(addr[1], end_addr, self.stack)
        d.run()
        # if end_addr.opcode == RETURN_VALUE:
        #     return end_addr[2]
        right = self.stack.pop()
        if isinstance(right, PyCompare) and right.extends(left):
            py_and = left.chain(right)
        else:
            py_and = PyBooleanAnd(left, right)
        self.stack.push(py_and)
        return end_addr

    # This appears when there are chained comparisons, e.g. 1 <= x < 10

    def JUMP_FORWARD(self, addr, delta):
        ## if delta == 2 and addr[1].opcode == ROT_TWO and addr[2].opcode == POP_TOP:
        ##     # We're in the special case of chained comparisons
        ##     return addr[3]
        ## else:
        ##     # I'm hoping its an unused JUMP in an if-else statement
        ##     return addr[1]
        return addr.jump()

    # or operator

    def JUMP_IF_TRUE_OR_POP(self, addr, target):
        end_addr = addr.jump()
        self.push_popjump(True, end_addr, self.stack.pop())
        left = self.pop_popjump()
        d = SuiteDecompiler(addr[1], end_addr, self.stack)
        d.run()
        right = self.stack.pop()
        self.stack.push(PyBooleanOr(left, right))
        return end_addr

    #
    # If-else statements/expressions and related structures
    #

    def POP_JUMP_IF(self, addr: Address, target: int, truthiness: bool) -> Union[Address, None]:
        jump_addr = addr.jump()
        end_of_loop = jump_addr.opcode == FOR_ITER or jump_addr[-1].opcode == SETUP_LOOP
        if jump_addr.opcode == FOR_ITER:
            # We are in a for-loop with nothing after the if-suite
            # But take care: for-loops in generator expression do
            # not end in POP_BLOCK, hence the test below.
            jump_addr = jump_addr.jump()
        elif end_of_loop:
            # We are in a while-loop with nothing after the if-suite
            jump_addr = jump_addr[-1].jump()[-1]
        cond = self.stack.pop()
        if not addr.is_else_jump():


            # Handle generator expressions with or clause
            for_iter = addr.seek_back(FOR_ITER)
            if for_iter:
                end_of_for = for_iter.jump()
                if end_of_for.addr > addr.addr:
                    gen = jump_addr.seek_forward((YIELD_VALUE, LIST_APPEND), end_of_for)
                    if gen:
                        if not truthiness:
                            truthiness = not truthiness
                            if truthiness:
                                cond = PyNot(cond)
                        self.push_popjump(truthiness, jump_addr, cond)
                        return None

            self.push_popjump(truthiness, jump_addr, cond)
            # Dictionary comprehension
            if jump_addr.seek_forward(MAP_ADD):
                return None

            # Generator
            if jump_addr.seek_forward(YIELD_VALUE):
                return None

            # Generator
            if jump_addr.opcode != END_FINALLY and jump_addr[1] and jump_addr[1].opcode == JUMP_ABSOLUTE:
                return None

            a = addr[1]
            while a and a < jump_addr:
                if a.opcode in stmt_opcodes:
                    break
                if a.opcode in pop_jump_if_opcodes and a.arg >= addr.arg:
                    return None
                a = a[1]
            # if there are no nested conditionals and no else clause, write the true portion and jump ahead to the end of the conditional
            cond = self.pop_popjump()
            end_true = jump_addr
            if truthiness:
                cond = PyNot(cond)
            d_true = SuiteDecompiler(addr[1], end_true)
            d_true.run()
            stmt = IfStatement(cond, d_true.suite, None)
            self.suite.add_statement(stmt)
            return end_true
        # Increase jump_addr to pop all previous jumps
        self.push_popjump(truthiness, jump_addr[1], cond)
        cond = self.pop_popjump()
        end_true = jump_addr[-1]
        if truthiness:
            last_pj = addr.seek_back(pop_jump_if_opcodes)
            if last_pj and last_pj.arg == addr.arg and isinstance(cond, PyBooleanAnd) or isinstance(cond, PyBooleanOr):
                cond.right = PyNot(cond.right)
            else:
                cond = PyNot(cond)

        if end_true.opcode == RETURN_VALUE:
            end_false = jump_addr.seek_forward(RETURN_VALUE)
            if end_false and end_false[2] and end_false[2].opcode == RETURN_VALUE:
                d_true = SuiteDecompiler(addr[1], end_true[1])
                d_true.run()
                d_false = SuiteDecompiler(jump_addr,end_false[1])
                d_false.run()
                self.suite.add_statement(IfStatement(cond, d_true.suite, d_false.suite))

                return end_false[1]

        # - If the true clause ends in return, make sure it's included
        # - If the true clause ends in RAISE_VARARGS, then it's an
        # assert statement. For now I just write it as a raise within
        # an if (see below)
        if end_true.opcode in (RETURN_VALUE, RAISE_VARARGS, POP_TOP):
            # TODO: change
            # if cond: raise AssertionError(x)
            # to
            #     assert cond, x
            d_true = SuiteDecompiler(addr[1], end_true[1])
            d_true.run()
            self.suite.add_statement(IfStatement(cond, d_true.suite, Suite()))
            return jump_addr
        d_true = SuiteDecompiler(addr[1], end_true)
        d_true.run()
        if jump_addr.opcode == POP_BLOCK and not end_of_loop:
            # It's a while loop
            stmt = WhileStatement(cond, d_true.suite)
            self.suite.add_statement(stmt)
            return jump_addr[1]
        # It's an if-else (expression or statement)
        if end_true.opcode == JUMP_FORWARD:
            end_false = end_true.jump()
        elif end_true.opcode == JUMP_ABSOLUTE:
            end_false = end_true.jump()
            if end_false.opcode == FOR_ITER:
                # We are in a for-loop with nothing after the else-suite
                end_false = end_false.jump()[-1]
            elif end_false[-1].opcode == SETUP_LOOP:
                # We are in a while-loop with nothing after the else-suite
                end_false = end_false[-1].jump()[-1]
            if end_false.opcode == RETURN_VALUE:
                end_false = end_false[1]
        elif end_true.opcode == RETURN_VALUE:
            # find the next RETURN_VALUE
            end_false = jump_addr
            while end_false.opcode != RETURN_VALUE:
                end_false = end_false[1]
            end_false = end_false[1]
        elif end_true.opcode == BREAK_LOOP:
            # likely in a loop in a try/except
            end_false = jump_addr
        else:
            end_false = jump_addr
            # # normal statement
            # raise Exception("#ERROR: Unexpected statement: {} | {}\n".format(end_true, jump_addr, jump_addr[-1]))
            # # raise Unknown
            # jump_addr = end_true[-2]
            # stmt = IfStatement(cond, d_true.suite, None)
            # self.suite.add_statement(stmt)
            # return jump_addr or self.END_NOW
        d_false = SuiteDecompiler(jump_addr, end_false)
        d_false.run()
        if d_true.stack and d_false.stack:
            assert len(d_true.stack) == len(d_false.stack) == 1
            # self.write("#ERROR: Unbalanced stacks {} != {}".format(len(d_true.stack),len(d_false.stack)))
            assert not (d_true.suite or d_false.suite)
            # this happens in specific if else conditions with assigments
            true_expr = d_true.stack.pop()
            false_expr = d_false.stack.pop()
            self.stack.push(PyIfElse(cond, true_expr, false_expr))
        else:
            stmt = IfStatement(cond, d_true.suite, d_false.suite)
            self.suite.add_statement(stmt)
        return end_false or self.END_NOW

    def POP_JUMP_IF_FALSE(self, addr, target):
        return self.POP_JUMP_IF(addr, target, truthiness=False)

    def POP_JUMP_IF_TRUE(self, addr, target):
        return self.POP_JUMP_IF(addr, target, truthiness=True)

    def JUMP_ABSOLUTE(self, addr, target):
        # print("*** JUMP ABSOLUTE ***", addr)
        # return addr.jump()

        # TODO: print out continue if not final jump
        jump_addr = addr.jump()
        if jump_addr[-1].opcode == SETUP_LOOP:
            end_addr = jump_addr + jump_addr[-1].arg
            last_jump = self.scan_for_final_jump(jump_addr, end_addr[-1])
            if last_jump != addr:
                pass
        pass

    #
    # For loops
    #

    def GET_ITER(self, addr):
        pass

    def FOR_ITER(self, addr: Address, delta):
        if addr[-1] and addr[-1].opcode == RETURN_VALUE:
            # Dead code
            return self.END_NOW
        iterable = self.stack.pop()
        jump_addr = addr.jump()
        end_body = jump_addr
        if end_body.opcode != POP_BLOCK:
            end_body = end_body[-1]
        d_body = SuiteDecompiler(addr[1], end_body)
        for_stmt = ForStatement(iterable)
        d_body.stack.push(for_stmt)
        d_body.run()
        for_stmt.body = d_body.suite
        self.suite.add_statement(for_stmt)
        return jump_addr

    # Function creation

    def MAKE_FUNCTION_OLD(self, addr, argc, is_closure=False):
        testType = self.stack.pop().val
        if isinstance(testType, str):
            code = Code(self.stack.pop().val, self.code)
        else:
            code = Code(testType, self.code)
        closure = self.stack.pop() if is_closure else None
        # parameter annotation objects
        paramobjs = {}
        paramcount = (argc >> 16) & 0x7FFF
        if paramcount:
            paramobjs = dict(zip(self.stack.pop().val, self.stack.pop(paramcount - 1)))
        # default argument objects in positional order 
        defaults = self.stack.pop(argc & 0xFF)
        # pairs of name and default argument, with the name just below the object on the stack, for keyword-only parameters 
        kwdefaults = {}
        for i in range((argc >> 8) & 0xFF):
            k, v = self.stack.pop(2)
            if hasattr(k, 'name'):
                kwdefaults[k.name] = v
            elif hasattr(k, 'val'):
                kwdefaults[k.val] = v
            else:
                kwdefaults[str(k)] = v
        func_maker = code_map.get(code.name, DefStatement)
        self.stack.push(func_maker(code, defaults, kwdefaults, closure, paramobjs))

    def MAKE_FUNCTION_NEW(self, addr, argc, is_closure=False):
        testType = self.stack.pop().val
        if isinstance(testType, str):
            code = Code(self.stack.pop().val, self.code)
        else:
            code = Code(testType, self.code)
        closure = self.stack.pop() if is_closure else None
        annotations = {}
        kwdefaults = {}
        defaults = {}
        if argc & 8:
            annotations = list(self.stack.pop())
        if argc & 4:
            annotations = self.stack.pop()
            if isinstance(annotations, PyDict):
                annotations = {str(k[0].val).replace('\'', ''): str(k[1]) for k in annotations.items}
        if argc & 2:
            kwdefaults = self.stack.pop()
            if isinstance(kwdefaults, PyDict):
                kwdefaults = {str(k[0].val): str(k[1] if isinstance(k[1], PyExpr) else PyConst(k[1])) for k in
                              kwdefaults.items}
            if not kwdefaults:
                kwdefaults = {}
        if argc & 1:
            defaults = list(map(lambda x: str(x if isinstance(x, PyExpr) else PyConst(x)), self.stack.pop()))
        func_maker = code_map.get(code.name, DefStatement)
        self.stack.push(func_maker(code, defaults, kwdefaults, closure, annotations, annotations))

    def MAKE_FUNCTION(self, addr, argc, is_closure=False):
        if sys.version_info < (3, 6):
            self.MAKE_FUNCTION_OLD(addr, argc, is_closure)
        else:
            self.MAKE_FUNCTION_NEW(addr, argc, is_closure)

    def LOAD_CLOSURE(self, addr, i):
        # Push the varname.  It doesn't matter as it is not used for now.
        self.stack.push(self.code.derefnames[i])

    def MAKE_CLOSURE(self, addr, argc):
        self.MAKE_FUNCTION(addr, argc, is_closure=True)

    #
    # Raising exceptions
    #

    def RAISE_VARARGS(self, addr, argc):
        # TODO: find out when argc is 2 or 3
        # Answer: In Python 3, only 0, 1, or 2 argument (see PEP 3109)
        if argc == 0:
            self.write("raise")
        elif argc == 1:
            exception = self.stack.pop()
            self.write("raise {}", exception)
        elif argc == 2:
            from_exc, exc = self.stack.pop(), self.stack.pop()
            self.write("raise {} from {}".format(exc, from_exc))
        else:
            raise Unknown

    def EXTENDED_ARG(self, addr, ext):
        # self.write("# ERROR: {} : {}".format(addr, ext) )
        pass

    def WITH_CLEANUP(self, addr, *args, **kwargs):
        # self.write("# ERROR: {} : {}".format(addr, args))
        pass

    def WITH_CLEANUP_START(self, addr, *args, **kwargs):
        pass

    def WITH_CLEANUP_FINISH(self, addr, *args, **kwargs):
        jaddr = addr.jump()
        return jaddr

    # Formatted string literals
    def FORMAT_VALUE(self, addr, flags):
        val = self.stack.pop()
        self.stack.push(PyFormatValue(val))

    def BUILD_STRING(self, addr, c):
        params = self.stack.pop(c)
        self.stack.push(PyFormatString(params))

    # Coroutines
    def GET_AWAITABLE(self, addr: Address):
        func: AwaitableMixin = self.stack.pop()
        func.is_awaited = True
        self.stack.push(func)
        yield_op = addr.seek_forward(YIELD_FROM)
        return yield_op[1]

    def BEFORE_ASYNC_WITH(self, addr: Address):
        with_addr = addr.seek_forward(SETUP_ASYNC_WITH)
        end_with = with_addr.jump()
        with_stmt = WithStatement(self.stack.pop())
        with_stmt.is_async = True
        d_with = SuiteDecompiler(addr[1], end_with)
        d_with.stack.push(with_stmt)
        d_with.run()
        with_stmt.suite = d_with.suite
        self.suite.add_statement(with_stmt)
        if sys.version_info <= (3, 4):
            assert end_with.opcode == WITH_CLEANUP
            assert end_with[1].opcode == END_FINALLY
            return end_with[2]
        else:
            assert end_with.opcode == WITH_CLEANUP_START
            assert end_with[1].opcode == GET_AWAITABLE
            assert end_with[4].opcode == WITH_CLEANUP_FINISH
            return end_with[5]

    def SETUP_ASYNC_WITH(self, addr: Address, arg):
        pass

    def GET_AITER(self, addr: Address):
        return addr[2]

    def GET_ANEXT(self, addr: Address):
        iterable = self.stack.pop()
        for_stmt = ForStatement(iterable)
        for_stmt.is_async = True
        jump_addr = addr[-1].jump()
        d_body = SuiteDecompiler(addr[3], jump_addr[-1])
        d_body.stack.push(for_stmt)
        d_body.run()
        jump_addr = jump_addr[-1].jump()
        new_start = jump_addr
        new_end = jump_addr[-2].jump()[-1]
        d_body.start_addr = new_start

        d_body.end_addr = new_end

        d_body.run()

        for_stmt.body = d_body.suite
        self.suite.add_statement(for_stmt)
        new_end = new_end.seek_forward(POP_BLOCK)
        return new_end


def make_dynamic_instr(cls):
    def method(self, addr):
        cls.instr(self.stack)

    return method


# Create unary operators types and opcode handlers
for op, name, ptn, prec in unary_ops:
    name = 'Py' + name
    tp = type(name, (PyUnaryOp,), dict(pattern=ptn, precedence=prec))
    globals()[name] = tp
    setattr(SuiteDecompiler, op, make_dynamic_instr(tp))

# Create binary operators types and opcode handlers
for op, name, ptn, prec, inplace_ptn in binary_ops:
    # Create the binary operator
    tp_name = 'Py' + name
    tp = globals().get(tp_name, None)
    if tp is None:
        tp = type(tp_name, (PyBinaryOp,), dict(pattern=ptn, precedence=prec))
        globals()[tp_name] = tp

    setattr(SuiteDecompiler, 'BINARY_' + op, make_dynamic_instr(tp))
    # Create the in-place operation
    if inplace_ptn is not None:
        inplace_op = "INPLACE_" + op
        tp_name = 'InPlace' + name
        tp = type(tp_name, (InPlaceOp,), dict(pattern=inplace_ptn))
        globals()[tp_name] = tp
        setattr(SuiteDecompiler, inplace_op, make_dynamic_instr(tp))

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print('USAGE: {} <filename.pyc>'.format(sys.argv[0]))
    else:
        print(decompile(sys.argv[1]))
