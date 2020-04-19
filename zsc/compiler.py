import io
import ast
import logging

from .prepass import ParseError, Prepass


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


WARN_ON_COMPARISONS = True

VERSION = '0.1.0'

class Analyzer(ast.NodeVisitor):
    def __init__(self, indent=0, input_file='', context=None, prepass=None):
        self.input_file = input_file
        self.indent = indent
        self.context = context
        self.stack = []
        self.defined = []
        self.prepass = prepass # an instance of the prepass visitor which collects all the function calls


        # these are functions which we recognize in input calls and convert to their
        # zbrush equivalents.  Not all have exact equivalents -- some zbrush
        # functions are represents by python syntac instead

        # todo: As written we only check these against the name of a call, ie,
        # it could be 'zrush.sin()` or `math.sin()` in the python side.  We should
        # probably regularize that for consistency & readability

        self.funcs = {
            "sin": "SIN",
            "cos": "COS",
            "tan": "TAN",
            "asin": "ASIN",
            "acos": "ACOS",
            "atan": "ATAN",
            "atan2": "ATAN2",
            "log": "LOG",
            "log10": "LOG10",
            "sqrt": "SQRT",
            "abs": "ABS",
            "random": "RAND",
            "randint": "IRAND",
            "bool": "BOOL",
            "int": "INT",
            "frac": "FRAC",
            'min': 'MIN',
            'max': 'MAX'
        }

        self.top_level_defs = []

        if self.context:
            self.input_file = self.context.input_file
            self.defined = self.context.defined
            self.funcs = self.context.funcs
            self.top_level_defs = self.context.top_level_defs
            self.prepass = self.context.prepass

    def format(self):
        "newline separated list, with tabs"
        def yield_values():
            for s in self.stack:
                yield self.tab() + s
        return '\n'.join(yield_values())

    def format_inline(self, sep=", "):
        """ comma separated list"""
        result = sep.join(self.stack)
        return result

    def tab(self, extra=0):
        return '    ' * (self.indent + extra)

    def visit_Import(self,  node):

        for name in node.names:
            if 'zbrush' in name.name:
                zname = name.name.split(".")[-1]
                self.funcs[name.asname or name.name] = zname

    def visit_ImportFrom(self, node):

        if node.module == 'zbrush':
            for name in node.names:
                self.funcs[name.asname or name.name] = name.name

    def visit_Return(self, node):
        """
        There's not equivalent of 'return values' in zbrush, so abort if the
        python script tries to return values. Otherwise, return an [Exit]
        """
        if node.value:
            self.abort(f"zscript does not support return values", node)
        self.stack.append("[Exit]")

    def visit_Assert(self, node):
        """
        Asserts
        """
        test = self.sub_parser(node.test)
        test_str = test.format_inline(sep=" ")
        self.stack.append(f'[Assert, {test_str}, "{node.msg.s}"]')

    def visit_For(self, node):

        iterator = node.iter
        if not isinstance(iterator, ast.Call) or iterator.func.id not in ('range', 'xrange'):
            self.abort("use range() to set loop iterations", node)

        loop_max = iterator.args[0].n
        loop_var = node.target.id

        self.stack.append("")
        self.stack.append(f'[Loop, {loop_max},')
        loop_parser = self.sub_parser(*node.body)
        if self.context:
            loop_parser.indent += 1

        # loop body
        self.stack.append(loop_parser.format())
        self.stack.append(self.tab() + ",")
        self.stack.append(self.tab() + f"{loop_var}")
        self.stack.append('] // loop end')

    def visit_Continue(self, node):
        self.stack.append('[LoopContinue]')

    def visit_Break(self, node):
        self.stack.append('[LoopExit]')

    def visit_FunctionDef(self, node):
        """
        Python def to zbrush [RoutineDef], with indented statements
        and appended in-out arguments
        """

        incoming_args = [j.arg for j in node.args.args]
        arg_string = ', '.join(incoming_args)

        self.stack.append('')  # space before defs for readability

        # prepend the docstring
        doc = ast.get_docstring(node)
        if doc:
            for line in doc.split('\n'):
                self.stack.append(f"// {line} ")

        self.stack.append('[RoutineDef, {},'.format(node.name))
        body_nodes = [e for e in node.body]
        # docstring will appear as an expression node
        # if present
        if doc:
            body_nodes = body_nodes[1:]
        sub_parse = self.sub_parser(*body_nodes)
        sub_parse.indent = self.indent + 1
        self.stack.append(sub_parse.format())

        if arg_string:
            self.stack.append(f'{self.tab(1)}, // args ')
            self.stack.append(f'{self.tab(1)}{arg_string}')
        self.stack.append(f"] // end {node.name}")
        self.stack.append('')

    def visit_Num(self, node):
        """
        numeric literals
        """
        self.stack.append("{}".format(node.n))

    def visit_Interactive(self, node):
        """"
        won't show up in raw code, used as a generic node
        container for sub-parsers
        """
        self.generic_visit(node)

    def visit_Str(self, node):
        """
        Make sure string literals have quotes
        """
        self.stack.append('\"{}\"'.format(node.s))

    def visit_Name(self, node):
        """
        Convert python name refereences to [Var, name]
        """
        # Q: when to use 'Val' instead?
        # Q: should we use #character?

        self.stack.append("[Var, {}]".format(node.id))

    def get_setter(self, name):
        if self.context or name in self.defined:
            return 'VarSet'

        self.defined.append(name)
        return "VarDef"

    def visit_BinOp(self, node):
        '''
        Format zbrush supported math operators
        '''
        # Q: Do we want 'val' instead of 'var' here?
        try:
            op = {
                ast.Add: '+',
                ast.Sub:  '-',
                ast.Mult: '*',
                ast.Div:  '/',
                ast.Pow: '^^',
                ast.And:  '&& ',
                ast.Or:   '||'
            }[type(node.op)]

            left = self.sub_parser(node.left)
            right = self.sub_parser(node.right)

            self.stack.append(
                f"({left.format_inline(sep= ' ')} {op} {right.format_inline(sep = ' ')})")
        except:
            self.abort(
                "ZBrush does not support operator {}".format(node.op), node)

    def visit_BoolOp(self, node):

        op = {
            ast.Or: '||',
            ast.And:  '&& '
        }[type(node.op)]

        left = self.sub_parser(node.values[0])
        right = self.sub_parser(node.values[1])

        self.stack.append(
            f'({left.format_inline(sep = " ")} {op} {right.format_inline(sep = " ")})')

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            target = self.as_literal(node.operand)
            self.stack.append(f"[NEG,{target} ]")
            return
        raise RuntimeError(f"Unsuporter oprations {node.op}")

    def visit_AugAssign(self, node):
        '''
        Convert python augmented assigns like

            variable += 5
        to
            [VarAdd, variable, 5]
        etc
        '''

        op = {
            ast.Add: 'Add',
            ast.Sub: 'Sub',
            ast.Mult: 'Mul',
            ast.Div: 'Div'
        }
        try:
            opstring = op[type(node.op)]
        except:
            self.abort(
                "ZBrush does not support augmented operator {}".format(node.op), node)

        target_var = node.target.id
        val = node.value

        parser = self.sub_parser(val)
        target_value = parser.format_inline()

        self.stack.append(f'[Var{opstring}, {target_var}, {target_value}]')

    def format_mem_op(self, method):
        '''
        helper method convert, eg, 

            some_mem_block.read_string(offset)

        to

            [MemReadString, some_mem_block, offset]

        or 

            some_mem_block.write_ulong(value)

        to 

            [MemWrite, some_mem_block, value, 6]

        where '6' is the zbrush typecode for ulongs

        '''

        m_name, _,  m_type = method.partition("_")

        if m_name not in ('read', 'write', 'resize', 'move', 'delete', 'multi_write', 'create_from_file'):
            return None, None

        if m_type == 'string':
            return f'Mem{m_name.title()}String', None

        typecode = {
            'float': 0,
            'char': 1,
            'uchar': 2,
            'short': 3,
            'ushort': 4,
            'long': 5,
            'ulong': 6,
            'fixed': 7
        }.get(m_type, 0)
        return f'Mem{m_name.title()}', typecode

    def visit_Call(self, node):

        is_attrib = isinstance(node.func, ast.Attribute)
        is_zb = False  # is this a recognized call
        is_mem_call = False

        if is_attrib:
            owner_name = node.func.value.id
            func_name = node.func.attr
            is_mem_call = (owner_name != "zbrush")
        else:
            owner_name = ""
            func_name = node.func.id

        is_zb = owner_name == 'zbrush' or func_name in self.funcs

        # collect the arguments
        arg_parser = self.sub_parser(*node.args, func=True)
        arg_string = arg_parser.format_inline()
        if arg_string:
            arg_string = ", " + arg_string

        if is_zb:
            # it's a zbrush function.  de-alias in possible and return
            if func_name in self.funcs:
                func_name = self.funcs.get(node.func.id, func_name)
                sig = self.prepass.get_signature(func_name)
                logger.info(f'zbrush signature for {func_name}:\n\t {sig}')

            func_string = f'[{func_name}{arg_string}]'
            self.stack.append(func_string)
            return

        if not is_mem_call:
            # it's not a zbrush call or a memblock function,
            # so we assume it's a routine call
            func_string = '[RoutineCall, {}{}]' .format(func_name, arg_string)
            self.stack.append(func_string)
            return

        else:
            # this is an operation on a mem block
            m_name, typecode = self.format_mem_op(func_name)
            if not m_name:
                # this will fail on, eg, a random python imported function
                self.abort(
                    f"Unrecognized operation {owner_name}.{func_name}",  node)

            # we have to insert the appropriate type code for value types here
            arg_parse = self.sub_parser(*node.args, func=True)
            args = arg_parse.stack
            if typecode:
                args.insert(1, typecode)
            tail = ''
            if args:
                tail = ", ".join(args)
                tail = ", " + tail

            if 'Write' in m_name:
                self.stack.append(f'[{m_name}, {node.func.value.id}{tail}]')
            else:
                self.stack.append(f'[{m_name}, {node.func.value.id}{tail}]')

    def visit_Delete(self, node):
        self.stack.append(f'[MemDelete, {node.targets[0].id}]')

    def as_literal(self, val):
        if hasattr(val, 's'):
            return f'"{val.s}"'
        if hasattr(val, 'n'):
            return val.n
        if isinstance(val, ast.Name):
            return f'#{val.id}'

        raise ValueError(f"cannot parse {val} as literal")

    def handle_array_assign(self, node):
        """
        define or set array variables

            xxx = [1,2,3]

        becomes

            [VarDef, xxx(3), 1]
            [VarSet, xxx(0), 1]
            [VarSet, xxx(1), 2]
            [VarSet, xxx(2), 3]

        and 

            xxx = [3] * 10

        becomes

            [VarDef, xxx(10), 3]

        note that the original arrays need to be homogeneous examples 
        of numbers or strings or variable refs.  THe transpiler won't
        follow variable refs to check types
        """

        varname = node.targets[0].id
        setter = self.get_setter(varname)
        fill = 0
        emplace = []

        # TODO: type check the incoming arrays
        # to make sure they are homogeneous

        if isinstance(node.value, ast.List):
            count = len(node.value.elts)
            emplace = [i for i in node.value.elts]
            fill = self.as_literal(emplace[0])
        elif isinstance(node.value, ast.BinOp):
            if type(node.value.op) not in (ast.Mult, ast.Add):
                self.abort(
                    f"operator {node.value.op} not supported here",  node)
            op = node.value
            if not isinstance(op.left, ast.List):
                self.abort("could not assignment expression", node)
            if type(op.op) == ast.Mult:
                arr = [i for i in op.left.elts]
                original_arr = arr[:]
                arr *= op.right.n
                fill = self.as_literal(arr[0])
                count = len(arr)
                if len(original_arr) > 1:
                    emplace = [i for i in arr]
            elif type(op.op) == ast.Add:
                arr = [i for i in op.left.elts]
                arr += [k for k in op.right]
                fill = self.as_literal(arr[0])
                count = len(arr)
                emplace = [i for i in arr]
        else:
            self.abort(
                f"can only parse array literals or array literal muliplies ", node)
        self.stack.append(f"[{setter}, {varname}({count}), {fill}]")
        if emplace:
            for idx, item in enumerate(emplace):
                self.stack.append(
                    f"[VarSet, {varname}({idx}), {self.as_literal(item)}]")

    def visit_Assign(self, node):
        logger.debug(f"assign (line {node.lineno})")

        varval = (node.value)
        varname = (node.targets[0].id)
        setter = self.get_setter(varname)

        if isinstance(varval, ast.BinOp) and isinstance(varval.left, ast.List):
            #eg, xxx = [0] * 10
            self.handle_array_assign(node)
            return

        if isinstance(varval, ast.List):
            # eg xxx = [1,2,3]
            self.handle_array_assign(node)
            return

        if type(varval) in (ast.Num, ast.Str, ast.Name):
            # xxx = "A" 
            # xxx = 1
            # xxx = some_variable  
            varval = self.as_literal(varval)
            self.stack.append(f'[{setter}, {varname}, {varval}]')
            return

        if isinstance(varval, ast.BinOp):
            # xxx = a + b , etc
            parser = self.sub_parser(varval)
            subval = parser.format_inline()
            self.stack.append(f'[{setter}, {varname}, {subval}]')
            return

        if isinstance(varval, ast.UnaryOp) and isinstance(varval.op, ast.USub):
            target = self.as_literal(varval.operand)
            if isinstance(varval.operand, ast.Num):
                # a = -1 -> [VarSet, a, -1]
                self.stack.append (f"[{setter}, {varname}, -{target}]")
            else:  
                # a = -b -> [VarSet, a, [NEG, #b]]
                target = self.as_literal(varval.operand)
                self.stack.append (f"[{setter}, {varname}, [NEG, {target}]]")
            return

        if not isinstance(varval, ast.Call):
            self.abort(f"can't parse {varval}", node)

        # below here, we know it's a function call
        # that must be either a zbrush function with a return type
        # a math function (like 'sin' or 'cos')
        # or a memory read

        prefix, name = self.prepass.get_call_name(varval)
        logger.debug(f"assign call {prefix}.{name}")

        has_return = self.prepass.has_return_type(varval)
    
        logger.debug(f"is zfunc with return: {has_return}")
        if isinstance(varval.func, ast.Attribute):
            var_root = varname.split("(")[0]
            if self.context or (var_root in self.top_level_defs):
                setter = 'VarSet'
            else:
                setter = 'VarDef'
                self.top_level_defs.append(var_root)

            caller = varval.func.value.id

            is_mem_create = varval.func.attr == 'MemCreate'

            if is_mem_create:
                arg_parser = self.sub_parser(*varval.args)
                arg_string = arg_parser.format_inline()
                if arg_string:
                    arg_string = ", " + arg_string

                self.stack.append(f'[MemCreate, {varname}{arg_string}]')
                return

            arg_parse = self.sub_parser(*varval.args, func=True)
            if not has_return:
                
                mem_name, mem_op = self.format_mem_op(name)
                if not mem_name:
                    self.abort("can only call zbrush functions or memory block functions in an assignment", node)

                args = arg_parse.stack
                if mem_op:
                    args.insert(1, mem_op)
                tail = ''
                if args:
                    tail = ", ".join(args)
                    tail = ", " + tail
                self.stack.append(f'[{setter}, {varname}, [{mem_name}, {caller}{tail}]]')
                return
            else:
                _, funcname = self.prepass.get_call_name(varval)
                z_name = self.prepass.zbrush_aliases[funcname]
                args = arg_parse.stack
                tail = ''
                if args:
                    tail = ", ".join(args)
                    tail = ", " + tail
                self.stack.append(f'[{setter}, {varname}, [{z_name}{tail}]]')



    def visit_Lt(self, node):
        self.stack.append(" < ")

    def visit_Gt(self, node):
        self.stack.append(" > ")

    def visit_Lte(self, node):
        self.stack.append(" <=")

    def visit_Gte(self, node):
        self.stack.append(" >= ")

    def visit_Eq(self, node):
        self.stack.append(" = ")  # note, this is not a double equal!

    def visit_NotEq(self, node):
        self.stack.append(" != ")

    def visit_If(self, node):

        test = self.sub_parser(node.test)
        comp = ''.join(test.stack)

        body = self.sub_parser(*node.body)
        body_str = body.format() or ""

        orelse = self.sub_parser(*node.orelse)
        else_str = orelse.format() or ""

        self.stack.append('')
        self.stack.append(f"[If, ({comp}),")
        self.stack.append(f"{self.tab()}// then...")
        self.stack.append(body_str)
        self.stack.append(f"{self.tab() or '    '}, // else")
        self.stack.append(else_str)
        self.stack.append(']')

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            self.stack.append(f'// {node.value.s}')
        else:
            sub_parser = self.sub_parser(node.value)
            comp = ''.join(sub_parser.stack)
            self.stack.append(comp)

    def visit_While(self, node):
        # ZScript does not support a while loop.  So, we
        # loop a finite number of times checking the exit 
        # condifition. 
        # Todo:  rather than using int16 (65535) as the 
        # loop, allow user to set it with a constant from code?
        breakout = ast.If(
            test=node.test,
            body=[ast.Expr(value=ast.Continue())],
            orelse=[ast.Expr(value=ast.Break())]
        )

        body_block = [i for i in node.body]
        body_block.append(breakout)

        new_node = ast.For(
            target=ast.Name("WhileLoop"),
            iter=ast.Call(func=ast.Name(id="range"),
                          ctx=ast.Load(), args=[ast.Num(n=65534)]),
            body=body_block
        )
        #try:
            #self.indent -= 1
        subp = self.sub_parser(new_node)
        if not self.context:
            subp.indent -= 1
            #if not self.context:
            #    subp.indent -= 1
        self.stack.append(subp.format())
        #finally:
            #self.indent += 1




    def report(self):
        for item in self.stack:
            print(item)

    def abort(self, message, node):
        """
        fail the transpilation and print an error message
        """

        error_line = self.input_file.splitlines(
        )[node.lineno - 2: node.lineno + 1]
        raise ValueError("Compile Error: {} in line {}".format(
            message, node.lineno), error_line)

    def sub_parser(self, *args, **kwargs):
        if kwargs.get('func'):
            sub_parser = FunctionAnalyzer(context=self, prepass=self.prepass)
        else:
            sub_parser = Analyzer(context=self)
        sub_parser.indent += 1
        temp = ast.Interactive(list(args))
        sub_parser.visit(temp)
        return sub_parser


class FunctionAnalyzer(Analyzer):
    """
    a tweaked versions which preserves variable names
    """

    def visit_Name(self, node):
        if self.prepass.is_user_function(node):
            # for UI Elements or other items that expect command lists,
            # python code should make a no-arg function and pass it 
            # directly, ie,
            # 
            #   def test():
            #       zbrush.Note("OK") 
            #
            #   zBrush.IButton("Test", "", test)

            self.stack.append(f"[RoutineCall, {node.id}]")
        else:
            # for variables passed as arguments to a function, use the # prefix
            self.stack.append(f"#{node.id}")



def compile(filename, out_filename=''):

    with open(filename, "r") as source:
        input_file = source.read()

    tree = ast.parse(input_file)

    prepass = Prepass()
    prepass.visit(tree)

    print (prepass.user_functions)
    print (prepass.module_aliases)

    analyzer = Analyzer(0, input_file=input_file, prepass=prepass)
    analyzer.visit(tree)

    out_filename = out_filename or filename.replace('.py', '.txt')

    with open(out_filename, 'wt') as output:
        tp = (f'transpiled with zsc {VERSION}')
        orig = f'from: {filename}'

        output.write(f"// {tp}\n// {orig}\n")
        output.write(analyzer.format())

    return out_filename, analyzer.format()

