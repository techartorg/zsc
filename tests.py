import unittest
import zsc.prepass as prepass
import zsc.compiler as compiler
import ast
import inspect


class TestPrepass(unittest.TestCase):

    def test_get_call_name_zfunc(self):
        p = prepass.Prepass()
        example = ast.parse('''zbrush.IClick("a:b:c")''', mode='eval')
        assert (p.get_call_name(example.body)) == ('zbrush', 'IClick')

    def test_get_call_name_raw(self):
        p = prepass.Prepass()
        example = ast.parse('''somefunction()''', mode='eval')
        assert (p.get_call_name(example.body)) == ('', 'somefunction')

    def test_get_is_zfunc_normal(self):
        p = prepass.Prepass()
        raw = '''import zbrush\nzbrush.IClick()'''
        p.visit(ast.parse(raw))
        example = ast.parse('''zbrush.IClick("A")''', mode='eval')
        assert (p.is_zbrush_function(example.body))

    def test_get_is_zfunc_fail_unrecognized(self):
        p = prepass.Prepass()
        raw = '''import zbrush\nzbrush.IClick()'''
        p.visit(ast.parse(raw))
        example = ast.parse('''dummy("A")''', mode='eval')
        assert (not p.is_zbrush_function(example.body))

    def test_get_zfunc_mod_alias(self):
        p = prepass.Prepass()
        raw = '''import zbrush as zb\nzb.IClick()'''
        p.visit(ast.parse(raw))
        example = ast.parse('''zb.IClick("A")''', mode='eval')
        assert (p.is_zbrush_function(example.body))

    def test_get_zfunc_func_alias(self):
        p = prepass.Prepass()
        raw = '''from zbrush import IClick as blah'''
        p.visit(ast.parse(raw))
        example = ast.parse('''blah("A")''', mode='eval')
        assert (p.is_zbrush_function(example.body))

    def test_get_zfunc_signature(self):
        p = prepass.Prepass()
        raw = '''from zbrush import IClick as blah'''
        p.visit(ast.parse(raw))
        assert isinstance(p.get_signature('IClick'), inspect.FullArgSpec)

    def test_allows_zbrush_import(self):
        p = prepass.Prepass()
        raw = '''import zbrush'''
        p.visit(ast.parse(raw))

    def test_allows_math_import(self):
        p = prepass.Prepass()
        raw = '''import math'''
        p.visit(ast.parse(raw))

    def test_allows_random_import(self):
        p = prepass.Prepass()
        raw = '''import random'''
        p.visit(ast.parse(raw))

    def test_no_other_import_plain(self):
        p = prepass.Prepass()
        raw = '''import csv'''
        def bad(): return p.visit(ast.parse(raw))
        self.assertRaises(prepass.ParseError, bad)

    def test_no_other_math_import_aliased(self):
        p = prepass.Prepass()
        raw = '''import csv as xyz'''
        def bad(): return p.visit(ast.parse(raw))
        self.assertRaises(prepass.ParseError, bad)

    def test_user_function(self):
        p = prepass.Prepass()
        raw = '''def userfunc():\n    return 1'''
        p.visit(ast.parse(raw))
        call = ast.Call(ast.Name("userfunc"))
        assert p.is_user_function(call)

    def test_user_function_negative(self):
        p = prepass.Prepass()
        raw = '''def userfunc():\n    return 1'''
        p.visit(ast.parse(raw))
        call = ast.Call(ast.Name("not_userfunc"))
        assert not p.is_user_function(call)

    def test_has_return_type(self):
        p = prepass.Prepass()
        raw = '''import zbrush, math, random'''
        p.visit(ast.parse(raw))
        call = ast.Call(ast.Name("GetActiveToolPath"))
        assert p.has_return_type(call)

    def test_has_return_type_neg(self):
        p = prepass.Prepass()
        raw = '''import zbrush, math, random'''
        p.visit(ast.parse(raw))
        call = ast.Call(ast.Name("MTransformSet"))
        assert not p.has_return_type(call)

    def test_return_type_math(self):
        p = prepass.Prepass()
        raw = '''import zbrush, math, random'''
        p.visit(ast.parse(raw))
        call = ast.Call(ast.Name("sin"))
        assert p.has_return_type(call)

    def test_return_type_random(self):
        p = prepass.Prepass()
        raw = '''import zbrush, math, random'''
        p.visit(ast.parse(raw))
        call = ast.Call(ast.Name("randint"))
        assert p.has_return_type(call)

    def test_return_type_user(self):
        # note that user functions _CANT_ have return types
        # in zbrush, so this ignores the python.  The compiler
        # raises an error for this
        p = prepass.Prepass()
        raw = '''def userfunc():\n    return 1'''
        p.visit(ast.parse(raw))
        call = ast.Call(ast.Name("usefunc"))
        assert not p.has_return_type(call)



class TestAnalyzer(unittest.TestCase):

    def parse (self, stringval):
        tree = ast.parse(stringval)
        p = prepass.Prepass()
        p.visit(tree)
        analyzer = compiler.Analyzer(0, input_file="dummy", prepass=p)
        return analyzer, tree



    def test_assign_int(self):
        analyzer, tree  = self.parse('''a = 1''')
        analyzer.visit(tree)
        assert analyzer.format() == '[VarDef, a, 1]'

    def test_assign_float(self):
        analyzer, tree  = self.parse('''a = -1.0''')
        analyzer.visit(tree)
        assert analyzer.format() == '[VarDef, a, -1.0]'
    
    def test_assign_str(self):
        analyzer, tree  = self.parse('''a = "fred"''')
        analyzer.visit(tree)
        assert analyzer.format() == '[VarDef, a, "fred"]'

    def test_assign_var(self):
        analyzer, tree  = self.parse('''a = 1\nb = a''')
        analyzer.visit(tree)
        assert analyzer.format() == '[VarDef, a, 1]\n[VarDef, b, #a]'

    def test_assign_var_neg(self):
        analyzer, tree  = self.parse('''a = 1\nb = -a''')
        analyzer.visit(tree)
        assert analyzer.format() == '[VarDef, a, 1]\n[VarDef, b, [NEG, #a]]'

    def test_assign_def_vs_set(self):
        # use VarDef at the top level but VarSet inside of functions
        analyzer, tree  = self.parse('''a = 1\ndef func(input, output):\n    temp = input + 1\n    output = temp''')
        analyzer.visit(tree)
        result =  analyzer.format()
        assert '[VarDef, a, 1]' in result
        assert '[VarSet, temp, ' in result
        assert '[VarSet, output' in result



if __name__ == '__main__':
    unittest.main()
