"""test for utils module"""

try:
    import numpy as np
except:
    np = None
    
import unittest

from modelparameters.logger import suppress_logging
from modelparameters.utils import *

suppress_logging()

def dummy():pass

class RangeTests(unittest.TestCase):
    def test_wrong_init(self):
        with self.assertRaises(ValueError) as cm:
            Range(gt=0, ge=1)
        self.assertEqual(str(cm.exception), "Cannot create a 'Range' "\
                         "including both 'ge' and 'gt'")
        with self.assertRaises(ValueError) as cm:
            Range(lt=0, le=1)
        self.assertEqual(str(cm.exception), "Cannot create a 'Range' "\
                         "including both 'le' and 'lt'")
        with self.assertRaises(TypeError) as cm:
            Range(lt="")
        self.assertEqual(str(cm.exception), "expected a scalar for the 'lt' arg")

        with self.assertRaises(ValueError) as cm:
            Range(lt=10, ge=100)
        self.assertEqual(str(cm.exception), "expected the maxval to be larger"\
                         " than minval")

    def test_comp(self):
        self.assertEqual(Range(gt=0), Range(gt=0))
        self.assertEqual(repr(Range(gt=0)), "Range(gt=0)")
        self.assertEqual(str(Range(gt=0)), "(0, \xe2\x88\x9e]")
        
    def test_range_check(self):
        self.assertTrue(0.1 in Range(gt=0))
        self.assertTrue(0.1 in Range(gt=0, lt=0.2))
        self.assertTrue(0.1 in Range(0, 0.2))
        self.assertTrue(0.1 in Range(le=0.2))
        self.assertEqual(Range(le=0.2).format(0.1),
                         "0.1 \xe2\x88\x88 [-\xe2\x88\x9e, 0.2]")
        self.assertEqual(Range(gt=0).format(inf),
                         "\xe2\x88\x9e \xe2\x88\x88 (0, \xe2\x88\x9e]")
        self.assertEqual(Range(gt=-0.2).format(-1),
                         "-1 \xe2\x88\x89 (-0.2, \xe2\x88\x9e]")

        if np is None:
            return

        array = np.arange(2,10)
        self.assertTrue(array in Range(gt=0))
        self.assertTrue(array in Range(gt=0, lt=20))
        self.assertTrue(array in Range(0, 20))
        self.assertTrue(array in Range(le=20))
        self.assertEqual(Range(le=20).format(array),
                         "[2, 3, ..., 8, 9] \xe2\x88\x88 [-\xe2\x88\x9e, 20]")
        
class CheckArgs(unittest.TestCase):
    def test_check_arg(self):

        with self.assertRaises(TypeError) as cm:
            check_arg(1, str)
        self.assertEqual(str(cm.exception), \
                         "expected 'str' (got '1' which is 'int')")

        with self.assertRaises(TypeError) as cm:
            check_arg(1, str, 0)
        self.assertEqual(str(cm.exception), "expected 'str' (got '1' which is "\
                         "'int') as the first argument")

        with self.assertRaises(TypeError) as cm:
            check_arg(["s"], list, itemtypes=int)
        self.assertEqual(str(cm.exception), "expected 'list' of 'int'")

        with self.assertRaises(TypeError) as cm:
            check_arg(1, str, 2)
        self.assertEqual(str(cm.exception), "expected 'str' (got '1' which is "\
                         "'int') as the third argument")

        with self.assertRaises(TypeError) as cm:
            check_arg(1, str, 2, CheckArgs.test_check_arg)
        self.assertEqual(str(cm.exception), "expected 'str' (got '1' which is "\
                         "'int') as the third argument while calling "\
                         "'CheckArgs.test_check_arg'")

        with self.assertRaises(TypeError) as cm:
            check_arg(1, str, 2, CheckArgs)
        self.assertEqual(str(cm.exception), "expected 'str' (got '1' which is "\
                         "'int') as the third argument while instantiating "\
                         "'CheckArgs'")

        with self.assertRaises(ValueError) as cm:
            check_arg(1, int, context=dummy, gt=2)
        self.assertEqual(str(cm.exception), "1 \xe2\x88\x89 (2, \xe2\x88\x9e] "\
                         "while calling 'dummy'")

        with self.assertRaises(ValueError) as cm:
            check_arg(1, int, gt=2, le=3)
        self.assertEqual(str(cm.exception), "1 \xe2\x88\x89 (2, 3]")

        with self.assertRaises(ValueError) as cm:
            check_arg(5, int, ge=2, lt=3)
        self.assertEqual(str(cm.exception), "5 \xe2\x88\x89 [2, 3)")

        self.assertIsNone(check_arg(1, int))
        self.assertIsNone(check_arg(1, scalars))
        self.assertIsNone(check_arg(1.0, scalars))
        self.assertIsNone(check_arg(1.0, (float, int)))
        self.assertIsNone(check_arg([1.0, 2.0], list, itemtypes=float))
        self.assertIsNone(check_arg(1.0, scalars, gt=0, lt=2))
        self.assertIsNone(check_arg(5, scalars, ge=0, le=10))

        if np is None:
            return

        self.assertIsNone(check_arg(np.arange(11), np.ndarray, ge=0, le=10))

    def test_check_kwarg(self):

        with self.assertRaises(TypeError) as cm:
            check_kwarg(1, "jada", str)
        self.assertEqual(str(cm.exception), \
                         "expected 'str' (got '1' which is 'int') "\
                         "as the 'jada' argument")

        with self.assertRaises(TypeError) as cm:
            check_kwarg(["s"], "jada", list, itemtypes=int)
        self.assertEqual(str(cm.exception), "expected 'list' of 'int' "\
                         "as the 'jada' argument")

        with self.assertRaises(TypeError) as cm:
            check_kwarg(1, "jada", str, CheckArgs.test_check_arg)
        self.assertEqual(str(cm.exception), "expected 'str' (got '1' which is "\
                         "'int') as the 'jada' argument while calling "\
                         "'CheckArgs.test_check_arg'")

        with self.assertRaises(TypeError) as cm:
            check_kwarg(1, "bada", str, CheckArgs)
        self.assertEqual(str(cm.exception), "expected 'str' (got '1' which is "\
                         "'int') as the 'bada' argument while instantiating "\
                         "'CheckArgs'")

        with self.assertRaises(ValueError) as cm:
            check_kwarg(1, "bada", int, context=dummy, gt=2)
        self.assertEqual(str(cm.exception), "1 \xe2\x88\x89 (2, \xe2\x88\x9e] "\
                         "as the 'bada' argument while calling 'dummy'")

        with self.assertRaises(ValueError) as cm:
            check_kwarg(1, "bada", int, gt=2, le=3)
        self.assertEqual(str(cm.exception), "1 \xe2\x88\x89 (2, 3] "\
                         "as the 'bada' argument")

        with self.assertRaises(ValueError) as cm:
            check_kwarg(5, "bada", int, ge=2, lt=3)
        self.assertEqual(str(cm.exception), "5 \xe2\x88\x89 [2, 3) "\
                         "as the 'bada' argument")

        self.assertIsNone(check_kwarg(1, "bada", int))
        self.assertIsNone(check_kwarg(1, "bada", scalars))
        self.assertIsNone(check_kwarg(1.0, "bada", scalars))
        self.assertIsNone(check_kwarg(1.0, "bada", (float, int)))
        self.assertIsNone(check_kwarg([1.0, 2.0], "bada", list, itemtypes=float))
        self.assertIsNone(check_kwarg([1.0, "jada"], "bada", list, \
                                      itemtypes=(float, str)))
        self.assertIsNone(check_kwarg(1.0, "bada", scalars, gt=0, lt=2))
        self.assertIsNone(check_kwarg(5, "bada", scalars, ge=0, le=10))

class BasicUtils(unittest.TestCase):
    def test_iterables(self):
        flatten = add_iterable(([i]*i for i in range(5)), [])
        self.assertEqual(flatten, [1,2,2,3,3,3,4,4,4,4])
        self.assertEqual(add_iterable(flatten, 0), 30)
        self.assertTrue(is_iterable(flatten))
        self.assertTrue(is_iterable([0,0]))
        self.assertTrue(is_iterable("jada"))
        self.assertFalse(is_iterable(None))
        self.assertFalse(is_iterable(1))
        
    def test_string_utils(self):
        self.assertEqual(camel_capitalize("jada_bada_snada"), "JadaBadaSnada")
        self.assertEqual(camel_capitalize("_jada_bada_snada"), "JadaBadaSnada")
        self.assertEqual(quote_join(["jada", "bada", "snada"]), "'jada', 'bada', 'snada'")

    def test_wraping(self):
        self.assertEqual(tuplewrap(0), (0,))
        self.assertEqual(tuplewrap((0,)), (0,))
        self.assertEqual(listwrap(0), [0,])
        self.assertEqual(listwrap([0,]), [0,])

    def test_time_format(self):
        self.assertEqual(format_time(60), '1 m')
        self.assertEqual(format_time(60.999), '1 m')
        self.assertEqual(format_time(59), '59 s')
        self.assertEqual(format_time(3600), '1 h')
        self.assertEqual(format_time(3600*4+5), '4 h 5 s')
        self.assertEqual(format_time(3600*24+5), '1 day 5 s')
        self.assertEqual(format_time(3600*24*3+5), '3 days 5 s')

    def test_tic(self):
        import time
        t0 = tic()
        time.sleep(0.1)
        self.assertTrue(.1<toc()<.2)
    
if __name__ == "__main__":
    unittest.main()
