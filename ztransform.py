"""
Transformers
"""

import ast
import pprint


class CompilationError(RuntimeError):
    pass


class ZAutoReturn(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.generic_visit(node)
        setattr(node, "zbrush", "routinedef")
        if not node.returns:
            return node

        node.args.args.append(ast.Name(id="_retval", ctx=ast.Load()))
        node.returns = ast.Name(id=f"auto_{node.returns.id}", ctx=ast.Load())
        self.recurse_insert_returns(node)
        return node

    def recurse_insert_returns(self, node):
        """
        recursively replaces return values
        with the _retval
        """
        inserts = []
        values = []
        for bnode in node.body:
            if hasattr(bnode, "body"):
                self.recurse_insert_returns(bnode)

        for idx, b in enumerate(node.body):
            if isinstance(b, ast.Return):
                inserts.append(idx)
                values.append(b.value)
        inserts.reverse()
        values.reverse(),
        for i, v in zip(inserts, values):
            t = ast.Assign(
                targets=[ast.Name("_retval", ctx=ast.Store())],
                value=v,
                type_comment=None,
            )

            node.body.insert(i, t)
            ast.increment_lineno(t)


class ZStripReturnValues(ast.NodeTransformer):

    def visit_Return(self, retnode):
        return ast.Return()


def apply_auto_returns(astnode):
    inserts = ZAutoReturn().generic_visit(astnode)
    return ZStripReturnValues().generic_visit(inserts)


class ZFuncs(ast.NodeTransformer):
    """
    strips "zbrush" from zfunc names,
    adds an attribute to identify them
    """

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Attribute):
            return node

        attrib = node.func
        if attrib.value.id != "zbrush":
            # if a helper module is imnplemented add it here
            raise CompilationError(
                f"line {node.lineno}: only the zbrush module is supported",
                ast.unparse(node),
            )

        test = ast.Call(
            ast.Name(attrib.attr.upper(), ctx=ast.Load()), args=node.args, keywords={}
        )
        setattr(test, "zbrush", "func")
        return test


class ZVarSet(ast.NodeTransformer):
    """
    turns assignments into zbrush setters
    """

    def visit_Module(self, mod):
        self.defs = set()

        for node in mod.body:
            if (isinstance, node, ast.Assign):
                self.defs.add(node)
        return mod

    def visit_Assign(self, node):
        if node in self.defs:
            return self.update_assign(node, "VarDef")
        else:
            return self.update_assign(node, "VarSet")

    def update_assign(self, node, setter):
        assignee = node.targets[0].id
        if assignee == "__":
            return node
        val = node.value
        call = ast.Call(
            func=ast.Name(setter, ast.Load()),
            args=[ast.Name(assignee, ast.Store()), val],
            keywords={},
        )
        node.targets = [ast.Name("__", ctx=ast.Store())]
        node.value = call
        setattr(node, "zbrush", setter)
        return node


class ZForLoop(node.NodeTransformer):
    def visit_For(self, node):
        # print(ast.dump(node))
        return node


test = '''
import zbrush

def test_xxx(arg):
    print ("i do nothing")
    zbrush.test(1,2,3)
    x = zbrush.test(4,5,6)
    return

def test_iterator(arg) -> int:
    for x in range(arg):
        if x == 3:
            return x * 2
    return  x == 1

bob = test_iterator(2)

def test_array_contains(arr, val) -> int:
    result = array_contains(arr, val)


# todo: figure out how to handle retruns in cases inside loops and whiles


def test_while(iterations, cutoff) -> int:
    val = 0
    """random internal comment"""
    otherval = 1.0
    while val < iterations:
        if val == cutoff:
            return val
        val += 1


def test_return_string(arg) -> str:
    """convert 'return val' to return an automatic value"""
    val = arg + "xxx"
    return val


def test_return_float(arg) -> float:
    """convert 'return val' to return an automatic value"""
    val = arg + 1.0
    return val


def test_return_int(arg) -> int:
    """convert 'return val' to return an automatic value"""
    val = arg + 1
    return val

'''

parsed = ast.parse(test)
print(ast.dump(parsed))
transformed = apply_auto_returns(parsed)
transformed = ZFuncs().generic_visit(transformed)
setter = ZVarSet()
transformed = setter.visit_Module(transformed)
transformed = setter.generic_visit(transformed)
# transformed = ZAutoReturnReturn().visit(parsed)
# pprint.pprint(ast.dump(transformed), indent=4)
print("-" * 80)
print(ast.unparse(transformed))
