"""test for parameters module"""

import unittest

from modelparameters.logger import suppress_logging
from modelparameters.utils import *
from modelparameters.parameterdict import *

try:
    import numpy as np
except:
    np = None

try:
    from modelparameters.sympytools import *
except:
    sp = None

suppress_logging()

def dummy():pass

def default_a():
    return ParameterDict(abla="sin", abli=123)

def default_b():
    return ParameterDict(bblal=987, 
                         bling=OptionParam("akjh", \
                                           ["akjh", "bla", "jada", "smada"]))

def default_params(sp=True):
    params = dict(
        something_very_long="3", 
        other=ScalarParam(.1239, le=10, gt=0), 
        a=default_a(), 
        b=default_b(), 
        const=ConstParam(3),
        )

    base0, base1 = None, None
    if sp:
        base0 = ScalarParam(5, gt=0, name="base0")
        base1 = ScalarParam(.5, gt=0, name="base1")
        params["zlave"] = base0.sym*base1.sym
    
    return base0, base1, ParameterDict(**params)

class TestParameterDict(unittest.TestCase):

    def test_init(self):

        cmp_str = """a = {
    abla = 'sin'
    abli =   123
}
b = {
    bblal =    987
    bling = 'akjh' \xe2\x88\x88 ['akjh', 'bla', 'jada', 'smada']
}
const           =      3 - Constant
other           = 0.1239 \xe2\x88\x88 (0, 10]
something_very_long =    '3'"""

        base0, base1, p = default_params(sp)
        if sp:
            cmp_str += "\nzlave           =    2.5 - SlaveParam(base0*base1)"

        self.assertEqual(str(p), cmp_str)

        p.b.bblal = 98
        p.b.bling = "jada"
        cmp_str = cmp_str.replace("987", " 98").replace(" 'akjh' ", " 'jada' ")
        self.assertEqual(str(p), cmp_str)

        # Test copy
        self.assertEqual(str(p.copy()), cmp_str)
        self.assertEqual(p.copy(True),
                         eval("{'a': {'abli': 123, 'abla': 'sin'}, "\
                              "'b': {'bblal': 98, 'bling': 'jada'}, "\
                              "'const': 3, 'something_very_long': '3', "\
                              "'zlave': 2.5, 'other': 0.1239}"))
        
        if sp:
            base1.value = 1.0
            cmp_str = cmp_str.replace("2.5", "5.0")
            self.assertEqual(str(p), cmp_str)

    def test_assignments(self):
        
        base0, base1, p = default_params(sp)

        # Wrong assignment
        with self.assertRaises(TypeError) as cm:
            p.b.bblal = "jada"
        self.assertEqual(str(cm.exception), "expected 'int' while setting "\
                         "parameter 'bblal'")
        
        with self.assertRaises(TypeError) as cm:
            p.b.bling = 98
        self.assertEqual(str(cm.exception), "expected 'str' while setting "\
                         "parameter 'bling'")
        
        with self.assertRaises(ValueError) as cm:
            p.b.bling = "snada"
        self.assertEqual(str(cm.exception), "Illegal value 'bling': 'snada' "\
                         "\xe2\x88\x89 ['akjh', 'bla', 'jada', 'smada']")

        with self.assertRaises(TypeError) as cm:
            p.b = "snada"
        self.assertEqual(str(cm.exception), "cannot overwrite a ParameterDict")

        # Const assignment
        p.const = 3
        with self.assertRaises(ValueError) as cm:
            p.const = 4
        self.assertEqual(str(cm.exception), "Illegal value 'const': 4 != 3")

        # Slave assigment
        with self.assertRaises(TypeError) as cm:
            p.zlave = 4
        self.assertEqual(str(cm.exception), "cannot assign to a SlaveParam")
        
        # Update
        p_old = p.copy()
        p.update(dict(a=dict(abli=122), c=dict(abli=111), d=45))

        for param, param_old in zip(p.iterparams(True), p_old.iterparams(True)):
            if param.name == "abli":
                self.assertNotEqual(param.value, param_old.value)
            else:
                self.assertEqual(param.value, param_old.value)

    def test_iteration(self):
        
        base0, base1, p = default_params(sp)

        self.assertEqual([param.name for param in p.iterparams()], \
                         ['const', 'other', 'something_very_long', 'zlave'])
        self.assertEqual([param.name for param in p.iterparams(recurse=True)],\
                         ['abla', 'abli', 'bblal', 'bling', 'const', 'other', \
                          'something_very_long', 'zlave'])
        self.assertEqual([param for param in p.iterparameterdicts()],\
                         [p.a, p.b])
        
    def test_optstr(self):
        
        base0, base1, p = default_params(sp)
        
        self.assertEqual(p.optstr(), " --a.abla sin --a.abli 123 --b.bblal 987 "\
                         "--b.bling akjh --other 0.1239 --something_very_long 3")

        p.parse_args(["--a.abla", "cos", "--b.bling", "smada"])

        self.assertEqual(p.a.abla, "cos")
        self.assertEqual(p.b.bling, "smada")

        with self.assertRaises(ValueError) as cm:
            p.parse_args(["--other", "-1"])
        self.assertEqual(str(cm.exception), "Trying to set 'other' while parsing "\
                         "command line, but Illegal value 'other': -1.0 "\
                         "\xe2\x88\x89 (0, 10]")
        
        p = ParameterDict(list=[1,2,3,4,5])
        p.parse_args(["--list", "-1", "1", "2"])
        self.assertEqual(p.list, [-1, 1, 2])
        
if __name__ == "__main__":
    unittest.main()
