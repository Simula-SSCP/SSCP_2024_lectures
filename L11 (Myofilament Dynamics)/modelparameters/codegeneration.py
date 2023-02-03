# Copyright (C) 2012 Johan Hake
#
# This file is part of ModelParameters.
#
# ModelParameters is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ModelParameters is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ModelParameters. If not, see <http://www.gnu.org/licenses/>.

# System imports
import sympy as sp
import re
from sympy.core.function import AppliedUndef as _AppliedUndef

from sympy.printing import StrPrinter as _StrPrinter
from sympy.printing.ccode import CCodePrinter as _CCodePrinter
from sympy.printing.latex import LatexPrinter as _LatexPrinter
from sympy.printing.latex import latex as _sympy_latex
from sympy.printing.precedence import precedence as _precedence

from modelparameters.utils import check_arg as _check_arg
from modelparameters.utils import scalars as _scalars

from distutils.version import LooseVersion as _V

_current_sympy_version = _V(sp.__version__)

# Check version for order arguments
if _current_sympy_version >= _V("0.7.2"):
    _order = "none"
else:
    _order = None

# A collection of language specific keywords
_cpp_keywords = ["auto", "const", "double", "float", "int", "short", "struct", 
                 "break", "continue", "else", "for", "long", "signed", "switch", 
                 "case", "default", "enum", "goto", "register", "sizeof", "typedef",
                 "char", "do", "extern", "if", "return", "static", "union", "while",
                 "asm", "dynamic_cast", "namespace", "reinterpret_cast", "try",
                 "bool", "explicit", "new", "static_cast", "typeid", "volatile",
                 "catch", "operator", "template", "typename",
                 "class", "friend", "private", "this", "using",
                 "const_cast", "inline", "public", "throw", "virtual",
                 "delete", "mutable", "protected", "wchar_t",
                 "or", "and", "xor", "not", "unsigned", "void"]

_python_keywords = ["and", "del", "from", "not", "while", "as", "elif", "global",
                    "or", "with", "assert", "else", "if", "pass", "yield",
                    "break", "except", "import", "print", "class", "exec",
                    "in", "raise", "continue", "finally", "is", "return", "def",
                    "for", "lambda", "try"]

_matlab_keywords = ["break", "case", "catch", "classdef", "continue", "else",
                    "elseif", "end", "for", "function", "global", "if", "otherwise",
                    "parfor", "persistent", "return", "spmd", "switch", "try", "while"]

_fortran_keywords = ["assign", "backspace", "block data", "call", "close", "common",
                     "continue", "data", "dimension", "do", "else", "else if", "end",
                     "endfile", "endif", "entry", "equivalence", "external", "format",
                     "function", "goto", "if", "implicit", "inquire", "intrinsic",
                     "open", "parameter", "pause", "print", "program", "read",
                     "return", "rewind", "rewrite", "save", "stop", "subroutine",
                     "then", "write"] + \
                     ["allocate", "allocatable", "case", "contains", "cycle",
                      "deallocate", "elsewhere", "exit", "include", "interface",
                      "intent", "module", "namelist", "nullify", "only", "operator",
                      "optional", "pointer", "private", "procedure", "public",
                      "result", "recursive", "select", "sequence", "target", "use",
                      "while", "where"] + \
                      ["forall", "pure"] + \
                      ["abstract", "associate", "asynchronous", "bind", "class",
                       "deferred", "enum", "enumerator", "extends", "final", "flush",
                       "generic", "import", "non_overridable", "nopass", "pass",
                       "protected", "value", "volatile", "wait"] + \
                       ["block", "codimension", "do concurrent", "contiguous",
                        "critical", "error stop", "submodule", "sync all",
                        "sync images", "sync memory", "lock", "unlock"]

_all_keywords = set(_cpp_keywords+_python_keywords+_matlab_keywords+_fortran_keywords)

def _get_potence(value):
    import math
    exponent = int(math.log10(value))/3*3
    rest = _round2(float(value)/10**exponent, 3)
    if rest < 1:
        exponent -= 3
        rest *= 1e3
    return rest, exponent

def _round2(x, n=0, sigs4n=1):
    """
    Return x rounded to the specified number of significant digits, n, as
    counted from the first non-zero digit. 
	
    If n=0 (the default value for round2) then the magnitude of the
    number will be returned (e.g. round2(12) returns 10.0).  
    
    If n<0 then x will be rounded to the nearest multiple of n which, by 
    default, will be rounded to 1 digit (e.g. round2(1.23,-.28) will round 
    1.23 to the nearest multiple of 0.3.
    
    Regardless of n, if x=0, 0 will be returned.
    """
    import math
	
    if x==0:
        return x
    if n<0:
        n=_round2(-n, sigs4n)
        return n*int(x/n+.5)
    if n==0:
        return 10.**(int(math.floor(math.log10(abs(x)))))
    return round(x, int(n) - 1 - int(math.floor(math.log10(abs(x)))))

def _coeff_isneg(a):
    """Return True if the leading Number is negative.

    Examples
    ========

    >>> from sympy.core.function import _coeff_isneg
    >>> from sympy import S, Symbol, oo, pi
    >>> _coeff_isneg(-3*pi)
    True
    >>> _coeff_isneg(S(3))
    False
    >>> _coeff_isneg(-oo)
    True
    >>> _coeff_isneg(Symbol('n', negative=True)) # coeff is 1
    False

    """

    if a.is_Mul:
        a = a.args[0]
    return a.is_Number and a.is_negative

_relational_map = {
    "==":"Eq",
    "!=":"Ne",
    "<":"Lt",
    "<=":"Le",
    ">":"Gt",
    ">=":"Ge",
    }

_relational_map_matlab = {
    "==":"==",
    "!=":"~=",
    "<":"<",
    "<=":"<=",
    ">":">",
    ">=":">=",
    }

def _print_Mul(self, expr):

    prec = _precedence(expr)
    
    if self.order not in ('old', 'none'):
        args = expr.as_ordered_factors()
    else:
        # use make_args in case expr was something like -x -> x
        args = sp.Mul.make_args(expr)

    args = tuple(args)

    if _coeff_isneg(expr):
        # If negative and -1 is the first arg: remove it
        if args[0].is_integer and int(args[0]) == 1:
            args = args[1:]
        else:
            args = (-args[0],) + args[1:]
        sign = "-"
    else:
        sign = ""
    
        # If first argument is Mul we do not want to add a parentesize
        if isinstance(args[0], sp.Mul):
            prec -= 1

    a = [] # items in the numerator
    b = [] # items that are in the denominator (if any)

    # Gather args for numerator/denominator
    for item in args:
        if item.is_commutative and item.is_Pow and item.exp.is_Rational and item.exp.is_negative:
            if item.exp != -1:
                b.append(sp.Pow(item.base, -item.exp, evaluate=False))
            else:
                b.append(sp.Pow(item.base, -item.exp))
        elif item.is_Rational and item is not sp.S.Infinity:
            if item.p != 1:
                a.append(sp.Rational(item.p))
            if item.q != 1:
                b.append(sp.Rational(item.q))
        else:
            a.append(item)

    a = a or [sp.S.One]

    a_str = map(lambda x:self.parenthesize(x, prec), a)
    b_str = map(lambda x:self.parenthesize(x, prec), b)

    if len(b) == 0:
        return sign + '*'.join(a_str)
    elif len(b) == 1:
        if len(a) == 1 and not (a[0].is_Atom or a[0].is_Add):
            return sign + "{0}/".format(a_str[0]) + '*'.join(b_str)
        else:
            return sign + '*'.join(a_str) + "/{0}".format(b_str[0])
    else:
        return sign + '*'.join(a_str) + "/({0})".format('*'.join(b_str))

# Patch sympy print Function
_old_print_Function = _StrPrinter._print_Function
def _print_Function(self, expr):
    if isinstance(expr, _AppliedUndef):
        return expr.func.__name__
    return _old_print_Function(self, expr)

#_StrPrinter._print_Function = _print_Function

_unit_template = re.compile(r"([a-zA-Z]+\*\*[\-0-9]+|[a-zA-Z]+)")
def latex_unit(unit):
    """
    Return sympified and LaTeX-formatted string describing given unit.
    E.g.:
    >>> LatexCodeGenerator.format_unit("m/s**2")
    '\\mathrm{\\frac{m}{s^{2}}}'
    """
    _check_arg(unit, str)
    if unit == "1":
        return ""
    atomic_units =[] 
    
    for unit in re.findall(_unit_template, unit):
        micro = False
        exp = 0

        # Check for usage of micro
        if "u" == unit[0]:
            unit = unit[1:]
            micro = True

        # Check for exponent
        if "**" in unit:
            unit, exp = unit.split("**")

        # Wrap text in mathrm
        unit = "\\mathrm{{{0}}}".format(unit)
        if exp:
            unit += "^{{{0}}}".format(exp)

        if micro:
            unit = "\\mu"+unit
            
        atomic_units.append(unit)

    return "\\,".join(atomic_units)

class _CustomPythonPrinter(_StrPrinter):
    def __init__(self, namespace=""):
        assert(namespace in ["", "math", "np", "numpy", "ufl"])
        self._namespace = namespace if not namespace else namespace + "."
        _StrPrinter.__init__(self, settings=dict(order=_order))
        
    def _print_Mod(self, expr):
        return "({0} % {1})".format(expr.args[0], expr.args[1])
        
    # Why is this not called!
    def _print_Log(self, expr):
        if self._namespace == "ufl.":
            return "{0}ln({1})".format(self._namespace,
                                       self._print(expr.base))
        else:
            return "{0}log({1})".format(self._namespace,
                                        self._print(expr.base))
    def _print_Abs(self, expr):
        if self._namespace == "math.":
            return "{0}fabs({1})".format(self._namespace, self.stringify(expr.args, ", "))
        elif self._namespace == "ufl.":
            return "abs({0})".format(self.stringify(expr.args, ", "))
        else:
            return "{0}abs({1})".format(self._namespace, self.stringify(expr.args, ", "))

    #def _print_One(self, expr):
    #    return "1.0"

    #def _print_Zero(self, expr):
    #    return "0.0"

    def _print_Float(self, expr):

        # If not finite we use parent printer
        if expr.is_zero:
            return "0"
        
        if not expr.is_finite:
            return _StrPrinter._print_Float(self, expr)

        return str(float(expr))
    #def _print_Integer(self, expr):
    #    return str(expr.p) + ".0"

    def _print_Derivative(self, expr):
        if not isinstance(expr.args[1], (_AppliedUndef, sp.Symbol)):
            error("Can only print Derivative code with a single dependent "\
                  "variabe. Got: {0}".format(sympycode(expr.args[1])))
        
        if isinstance(expr.args[0], _AppliedUndef):
            return "d%s_d%s" % (expr.args[0].func.__name__, "_".join(\
                self._print(arg) for arg in expr.args[1:]))
        return _StrPrinter._print_Derivative(self, expr)

    def _print_Subs(self, expr):
        # Execute subsitution
        orig_expr=expr.expr
        subs = dict((key,value) for key, value in zip(expr.variables, expr.point))
        return self._print(orig_expr.xreplace(subs))

    #def _print_NegativeOne(self, expr):
    #    return "-1.0"

    def _print_Sqrt(self, expr):
        return "{0}sqrt({1})".format(self._namespace, self._print(expr.args[0]))
    
    def _print_Relational(self, expr):
        return '{0}({1}, {2})'.format(_relational_map[expr.rel_op],
                                      self._print(expr.lhs), self._print(expr.rhs))
    def _print_Piecewise(self, expr):
        result = ""
        num_par = 0
        for e, c in expr.args[:-1]:
            num_par += 1
            result += "Conditional({0}, {1}, ".format(self._print(c), \
                                                      self._print(e))
        last_line = self._print(expr.args[-1].expr) + ")"*num_par
        return result+last_line

    def _print_And(self, expr):
        PREC = _precedence(expr)
        if self._namespace == "ufl.":
            if len(expr.args) != 2:
                error("UFL does not support more than 2 operands to And")
            return "ufl.And({0}, {1})".format(self._print(expr.args[0]),
                                              self._print(expr.args[1]))
        return "And({0})".format(", ".join(self._print(arg) for arg in expr.args[::-1]))

    def _print_Or(self, expr):
        PREC = _precedence(expr)
        if self._namespace == "ufl.":
            if len(expr.args) != 2:
                error("UFL does not support more than 2 operands to Or")
            return "ufl.Or({0}, {1})".format(self._print(expr.args[0]),
                                             self._print(expr.args[1]))
        return "Or({0})".format(", ".join(self._print(arg) for arg in expr.args[::-1]))

    def _print_Pow(self, expr, rational=False):
        PREC = _precedence(expr)
        if expr.exp.is_integer and int(expr.exp) == 1:
            return self.parenthesize(expr.base, PREC)
        if expr.exp is sp.S.NegativeOne:
            return "1.0/{0}".format(self.parenthesize(expr.base, PREC))
        if expr.exp.is_integer and int(expr.exp) in [2, 3]:
            return "({0})".format(\
                "*".join(self.parenthesize(expr.base, PREC) \
                         for i in xrange(int(expr.exp))), PREC)
        if expr.exp.is_integer and int(expr.exp) in [-2, -3]:
            return "1.0/({0})".format(\
                "*".join(self.parenthesize(expr.base, PREC) \
                         for i in xrange(-int(expr.exp))), PREC)
        if expr.exp is sp.S.Half and not rational:
            return "{0}sqrt({1})".format(self._namespace,
                                         self._print(expr.base))
        if expr.exp == -0.5:
            return "1/{0}sqrt({1})".format(self._namespace,
                                         self._print(expr.base))
        if self._namespace == "ufl.":
            return "{0}elem_pow({1}, {2})".format(self._namespace,
                                                  self._print(expr.base),
                                                  self._print(expr.exp))
        if self._namespace in ["np.", "numpy."]:
            return "{0}power({1}, {2})".format(self._namespace,
                                               self._print(expr.base),
                                               self._print(expr.exp))
        
        return "{0}pow({1}, {2})".format(self._namespace,
                                         self._print(expr.base),
                                         self._print(expr.exp))

    _print_Function = _print_Function
    _print_Mul = _print_Mul

class _CustomPythonCodePrinter(_CustomPythonPrinter):

    def _print_sign(self, expr):
        if self._namespace == "ufl.":
            return "{0}sign({1})".format(self._namespace, \
                                         self._print(expr.args[0]))
        elif self._namespace in ["math.", "numpy.", "np."]:
            return "{0}copysign(1.0, {1})".format(self._namespace,
                                                  self._print(expr.args[0]))
        return "sign({0})".format(self._print(expr.args[0]))

    def _print_Mod(self, expr):
        if self._namespace == "math.":
            return "{0}fmod({1})".format(self._namespace, \
                                         self.stringify(expr.args, ", "))
        else:
            return "{0}mod({1})".format(self._namespace,
                                        self.stringify(expr.args, ", "))
        
    def _print_Min(self, expr):
        if self._namespace == "ufl.":
            return "ufl.{0}({1})".format(expr.func.__name__,\
                                     self.stringify(expr.args, ", "))
        return "{0}({1})".format(expr.func.__name__.lower(),\
                                 self.stringify(expr.args, ", "))

    def _print_Max(self, expr):
        if self._namespace == "ufl.":
            return "ufl.{0}({1})".format(expr.func.__name__,\
                                     self.stringify(expr.args, ", "))
        return "{0}({1})".format(expr.func.__name__.lower(),\
                                 self.stringify(expr.args, ", "))

    def _print_Function(self, expr):
        #print expr.func.__name__, expr.args
        func_name = expr.func.__name__

        if isinstance(expr, _AppliedUndef):
            return func_name
        
        elif func_name == "ceiling":
            return "{0}ceil({1})".format(self._namespace, \
                                         self.stringify(expr.args, ", "))
        elif func_name == "log":
            if self._namespace == "ufl.":
                return "{0}ln({1})".format(self._namespace,
                                           self._print(expr.args[0]))
            else:
                return "{0}log({1})".format(self._namespace,
                                            self._print(expr.args[0]))
        else:
            return "{0}{1}".format(self._namespace, \
                        func_name.lower() + \
                        "({0})".format(self.stringify(expr.args, ", ")))

    def _print_re(self, expr):
        assert len(expr.args) == 1
        return "({0}).real".format(self._print(expr.args[0]))

    def _print_im(self, expr):
        assert len(expr.args) == 1
        return "({0}).imag".format(self._print(expr.args[0]))

    def _print_Piecewise(self, expr):
        result = ""
        num_par = 0
        if self._namespace == "ufl.":
            for e, c in expr.args[:-1]:
                num_par += 1
                result += "ufl.conditional({0}, {1}, ".format(self._print(c), \
                                                             self._print(e))
        else:
            cond_str = "{0}all({{0}})".format(self._namespace) \
                       if self._namespace in ["np.", "numpy."] else "{0}"
            for e, c in expr.args[:-1]:
                num_par += 1
                result += "({0} if {1} else ".format(\
                    self._print(e), cond_str.format(self._print(c)))

        last_line = self._print(expr.args[-1].expr) + ")"*num_par
        return result+last_line

    def _print_Relational(self, expr):
        if self._namespace == "ufl.":
            return 'ufl.{0}({1}, {2})'.format(_relational_map[expr.rel_op].lower(),
                                              self._print(expr.lhs), self._print(expr.rhs))
        return "{0} {1} {2}".format(self.parenthesize(expr.lhs, _precedence(expr)),
                                    expr.rel_op,
                                    self.parenthesize(expr.rhs, _precedence(expr)))

    def _print_Pi(self, expr=None):
        return "{0}pi".format(self._namespace)

    def _print_And(self, expr):
        PREC = _precedence(expr)
        if self._namespace == "ufl.":
            if len(expr.args) != 2:
                error("UFL does not support more than 2 operands to And")
            return "ufl.And({0}, {1})".format(self._print(expr.args[0]),
                                              self._print(expr.args[1]))
        return " and ".join(self.parenthesize(arg, PREC) for arg in expr.args[::-1])
        return "{0} and {1}".format(self.parenthesize(expr.args[0], PREC),
                                    self.parenthesize(expr.args[1], PREC))

    def _print_Or(self, expr):
        PREC = _precedence(expr)
        if self._namespace == "ufl.":
            if len(expr.args) != 2:
                error("UFL does not support more than 2 operands to Or")
            return "ufl.Or({0}, {1})".format(self._print(expr.args[0]),
                                             self._print(expr.args[1]))
        return " or ".join(self.parenthesize(arg, PREC) for arg in expr.args[::-1])
        return "{0} or {1}".format(self.parenthesize(expr.args[0], PREC),
                                   self.parenthesize(expr.args[1], PREC))

    
class _CustomCCodePrinter(_StrPrinter):
    """
    Overload some ccode generation
    """
    
    def __init__(self, cpp=False, float_precision="double", **settings):
        super(_CustomCCodePrinter, self).__init__(settings=settings)
        self._prefix = "std::" if cpp else ""
        self._float_postfix = "" if float_precision == "double" else "f"

    def _print_Float(self, expr):
        f_str = _StrPrinter._print_Float(self, expr)
        return f_str + self._float_postfix

    def _print_One(self, expr):
        return "1."+self._float_postfix

    def _print_Zero(self, expr):
        return "0."+self._float_postfix

    def _print_Integer(self, expr):
        return "{0}.{1}".format(expr.p, self._float_postfix)

    def _print_NegativeOne(self, expr):
        return "-1."+self._float_postfix

    def _print_Rational(self, expr):
        return "{0}.{2}/{1}.{2}".format(expr.p, expr.q, self._float_postfix)

    def _print_Min(self, expr):
        "fmin and fmax is not contained in std namespace untill -ansi g++ 4.7"
        return "fmin({0})".format(self.stringify(expr.args, ", "))

    def _print_Max(self, expr):
        "fmin and fmax is not contained in std namespace untill -ansi g++ 4.7"
        return "fmax({0})".format(self.stringify(expr.args, ", "))

    def _print_Ceiling(self, expr):
        return "{0}ceil({1})".format(self._prefix, self.stringify(expr.args, ", "))
        
    def _print_Abs(self, expr):
        return "{0}fabs({1})".format(self._prefix, self.stringify(expr.args, ", "))

    def _print_Mod(self, expr):
        return "{0}fmod({1})".format(self._prefix, self.stringify(expr.args, ", "))

    def _print_Piecewise(self, expr):
        result = ""
        for e, c in expr.args[:-1]:
            result += "({0} ? {1} : ".format(self._print(c), self._print(e))
        last_line = "{0})".format(self._print(expr.args[-1].expr))
        return result+last_line
    
    def _print_Function(self, expr):
        #print expr.func.__name__, expr.args
        if isinstance(expr, _AppliedUndef):
            return expr.func.__name__
        
        return "%s" % self._prefix + expr.func.__name__.lower() + \
               "(%s)"%self.stringify(expr.args, ", ")
    
    def _print_Subs(self, expr):
        # Execute subsitution
        orig_expr=expr.expr
        subs = dict((key,value) for key, value in zip(expr.variables, expr.point))
        return self._print(orig_expr.xreplace(subs))

    def _print_Derivative(self, expr):
        if not isinstance(expr.args[1], (_AppliedUndef, sp.Symbol)):
            error("Can only print Derivative code with a single dependent "\
                  "variabe. Got: {0}".format(sympycode(expr.args[1])))
        
        if isinstance(expr.args[0], _AppliedUndef):
            return "d%s_d%s" % (expr.args[0].func.__name__, "_".join(\
                self._print(arg) for arg in expr.args[1:]))
        return _StrPrinter._print_Derivative(self, expr)

    def _print_Pow(self, expr, rational=False):
        PREC = _precedence(expr)
        if expr.exp.is_integer and int(expr.exp) == 1:
            return self.parenthesize(expr.base, PREC)
        if expr.exp is sp.S.NegativeOne:
            return "1.0/{0}".format(self.parenthesize(expr.base, PREC))
        if expr.exp.is_integer and int(expr.exp) in [2, 3]:
            return "({0})".format(\
                "*".join(self.parenthesize(expr.base, PREC) \
                         for i in xrange(int(expr.exp))), PREC)
        if expr.exp.is_integer and int(expr.exp) in [-2, -3]:
            return "1.0/({0})".format(\
                "*".join(self.parenthesize(expr.base, PREC) \
                         for i in xrange(-int(expr.exp))), PREC)
        if expr.exp is sp.S.Half and not rational:
            return "{0}sqrt({1})".format(self._prefix,
                                         self._print(expr.base))
        if expr.exp == -0.5:
            return "1/{0}sqrt({1})".format(self._prefix,
                                           self._print(expr.base))
        return "{0}pow({1}, {2})".format(self._prefix,
                                         self._print(expr.base),
                                         self._print(expr.exp))
    def _print_sign(self, expr):
        return "{0}copysign(1.0, {1})".format(self._prefix, \
                                              self._print(expr.args[0]))

    def _print_Pi(self, expr=None):
        return "M_PI"

    def _print_And(self, expr):
        PREC = _precedence(expr)
        return " && ".join(self.parenthesize(arg, PREC) for arg in expr.args[::-1])

    def _print_Or(self, expr):
        PREC = _precedence(expr)
        return " || ".join(self.parenthesize(arg, PREC) for arg in expr.args[::-1])

    def _print_re(self, expr):
        assert len(expr.args) == 1
        return "{0}creal({1})".format(self._prefix,
                                      self._print(expr.args[0]))

    def _print_im(self, expr):
        assert len(expr.args) == 1
        return "{0}cimag({1})".format(self._prefix,
                                      self._print(expr.args[0]))

    def _print_Symbol(self, expr):
        if expr.name == "I":
            return "I_"
        return expr.name

    _print_Mul = _print_Mul

class _CustomMatlabCodePrinter(_StrPrinter):
    """
    Overload some ccode generation
    """
    
    def __init__(self, **settings):
        super(_CustomMatlabCodePrinter, self).__init__(settings=settings)

    def _print_Float(self, expr):

        # If not finite we use parent printer
        if expr.is_zero:
            return "0"
        
        if not expr.is_finite:
            return _StrPrinter._print_Float(self, expr)

        return str(float(expr))
            
    def _print_Min(self, expr):
        return "min(%s)" % (self.stringify(expr.args, ", "))

    def _print_Max(self, expr):
        return "max(%s)" % (self.stringify(expr.args, ", "))

    def _print_Ceiling(self, expr):
        return "ceil(%s)" % (self.stringify(expr.args, ", "))
    
    def _print_Piecewise(self, expr):
        result = ""
        for e, c in expr.args[:-1]:
            result += "((%s)*(%s) + ~(%s)*"%(self._print(c), \
                                             self._print(e), self._print(c))
        last_line = "(%s))" % self._print(expr.args[-1].expr)
        return result+last_line
    
    def _print_Function(self, expr):
        #print expr.func.__name__, expr.args
        if isinstance(expr, _AppliedUndef):
            return expr.func.__name__
        
        return "%s(%s)" % (expr.func.__name__.lower(), self.stringify(\
            expr.args, ", "))
    
    def _print_Pow(self, expr):
        PREC = _precedence(expr)
        if expr.exp.is_integer and int(expr.exp) == 1:
            return self.parenthesize(expr.base, PREC)
        if expr.exp is sp.S.NegativeOne:
            return '1.0/{0}'.format(self.parenthesize(expr.base, PREC))
        
        if expr.exp == 0.5:
            return 'sqrt({0})'.format(self._print(expr.base))

        # FIXME: Fix paranthesises
        return '{0}^{1}'.format(self.parenthesize(expr.base, PREC),
                                  self.parenthesize(expr.exp, PREC))
    def _print_And(self, expr):
        PREC = _precedence(expr)
        return " & ".join(self.parenthesize(arg, PREC) for arg in expr.args[::-1])

    def _print_Not(self, expr):
        PREC = _precedence(expr)
        return "~" + self.parenthesize(expr.args[0], PREC)

    def _print_Relational(self, expr):
        return "{0} {1} {2}".format(self.parenthesize(expr.lhs, _precedence(expr)),
                                    _relational_map_matlab[expr.rel_op],
                                    self.parenthesize(expr.rhs, _precedence(expr)))

        return '{0}({1}, {2})'.format(_relational_map_matlab[expr.rel_op],
                                      self._print(expr.lhs), self._print(expr.rhs))
    def _print_Or(self, expr):
        PREC = _precedence(expr)
        return " | ".join(self.parenthesize(arg, PREC) for arg in expr.args[::-1])

    def _print_re(self, expr):
        assert len(expr.args) == 1
        return "real({0})".format(self._print(expr.args[0]))

    def _print_im(self, expr):
        assert len(expr.args) == 1
        return "imag({0})".format(self._print(expr.args[0]))

    _print_Mul = _print_Mul

class _CustomLatexPrinter(_LatexPrinter):

    @staticmethod
    def _number_to_latex(value):

        if value < 0:
            sign = "-"
            value = -value
        else:
            sign = ""

        if abs(value) < 1e-32:
            rest, exponent = 0., 0
        else:
            rest, exponent = _get_potence(value)

        # If formating 0.322
        if exponent == -3 and int(rest) / 100 > 0:
            exponent = 0
            rest = float(rest)/1000

        # Format rest
        if rest >= 100:
            form = "%d"
            rest = int(rest)
        elif rest >=10:
            if rest % 1 > 0:
                form = "%.1f"
            else:
                form = "%d"
                rest = int(rest)
        else:
            if rest % 1 > 0:
                if (rest*10) % 1 > 0:
                    form = "%.2f"
                else:
                    form = "%.1f"
            else :
                form = "%d"
                rest = int(rest)
        if exponent == 0:
            return sign+form%rest
        
        return r"%s\!\times\!10 ^{%d}"%(sign+form%rest, exponent)
    
    def _needs_brackets(self, expr):
        """
        Returns True if the expression needs to be wrapped in brackets when
        printed, False otherwise. For example: a + b => True; a => False;
        10 => False; -10 => True.
        """
        return not ((expr.is_Integer and expr.is_nonnegative)
                    or (expr.is_Atom and expr is not sp.S.NegativeOne)
                    or (isinstance(expr, _AppliedUndef) and expr is not sp.S.NegativeOne))
    
    def _print_Integer(self, expr):
        return self._print_Float(expr.evalf())
    
    def _print_Float(self, expr):

        # If not finite we use parent printer
        if expr.is_zero:
            return "0"
        
        if not expr.is_finite:
            return _LatexPrinter._print_Float(self, expr)

        return self._number_to_latex(expr.evalf())
    
    def _print_Function(self, expr, *args, **kwargs):
        if isinstance(expr, _AppliedUndef):
            return self._print_Symbol(sp.Symbol(expr.func.__name__))
            return expr.func.__name__

        return _LatexPrinter._print_Function(self, expr, *args, **kwargs)

    def _print_Add(self, expr):
        terms = list(expr.args)
        tex = self._print(terms[0])

        for term in terms[1:]:
            out = self._print(term)
            if out and out[0] != "-":
                tex += " +"

            tex += " " + out

        return tex

    def _print_Mul(self, expr):
        coeff, _ = expr.as_coeff_Mul()

        if self.order not in ('old', 'none'):
            args = expr.as_ordered_factors()
        else:
            # use make_args in case expr was something like -x -> x
            args = sp.Mul.make_args(expr)
    
        args = tuple(args)

        if _coeff_isneg(expr):
            # If negative and -1 is the first arg: remove it
            if args[0].is_integer and int(args[0]) == 1:
                args = args[1:]
            else:
                args = (-args[0],) + args[1:]
            tex = "- "
        else:
            tex = ""

        expr = sp.Mul(*args)
        
        from sympy.simplify import fraction
        numer, denom = fraction(expr, exact=True)
        separator = self._settings['mul_symbol_latex']
        numbersep = self._settings['mul_symbol_latex_numbers']

        def convert(expr):

            # if expr is 1/1
            if expr.is_Pow and expr.exp.is_Rational and\
                   expr.exp.is_negative and expr.base is sp.S.One:
                expr = sp.S.One
                
            if not expr.is_Mul:
                return str(self._print(expr))
            else:
                _tex = last_term_tex = ""

                if self.order not in ('old', 'none'):
                    args = expr.as_ordered_factors()
                else:
                    args = expr.args

                for i, term in enumerate(args):
                    term_tex = self._print(term)

                    if self._needs_mul_brackets(term, last=(i == len(args) - 1)):
                        term_tex = r"\left(%s\right)" % term_tex

                    if re.search("[0-9][} ]*$", last_term_tex) and \
                            re.match("[{ ]*[-+0-9]", term_tex):
                        # between two numbers
                        _tex += numbersep
                    elif _tex:
                        _tex += separator

                    _tex += term_tex
                    last_term_tex = term_tex
                return _tex

        if denom is sp.S.One:
            tex += convert(numer)
        else:
            snumer = convert(numer)
            sdenom = convert(denom)
            ldenom = len(sdenom.split())
            ratio = self._settings['long_frac_ratio']
            if self._settings['fold_short_frac'] \
                    and ldenom <= 2 and not "^" in sdenom:
                # handle short fractions
                if self._needs_mul_brackets(numer, last=False):
                    tex += r"\left(%s\right) / %s" % (snumer, sdenom)
                else:
                    tex += r"%s / %s" % (snumer, sdenom)
            elif len(snumer.split()) > ratio*ldenom:
                # handle long fractions
                if self._needs_mul_brackets(numer, last=True):
                    tex += r"\frac{1}{%s}%s\left(%s\right)" \
                        % (sdenom, separator, snumer)
                elif numer.is_Mul:
                    # split a long numerator
                    a = sp.S.One
                    b = sp.S.One
                    for x in numer.args:
                        if self._needs_mul_brackets(x, last=False) or \
                                len(convert(a*x).split()) > ratio*ldenom or \
                                (b.is_commutative is x.is_commutative is False):
                            b *= x
                        else:
                            a *= x
                    if self._needs_mul_brackets(b, last=True):
                        tex += r"\frac{%s}{%s}%s\left(%s\right)" \
                            % (convert(a), sdenom, separator, convert(b))
                    else:
                        tex += r"\frac{%s}{%s}%s%s" \
                            % (convert(a), sdenom, separator, convert(b))
                else:
                    tex += r"\frac{1}{%s}%s%s" % (sdenom, separator, snumer)
            else:
                tex += r"\frac{%s}{%s}" % (snumer, sdenom)

        return tex

    def _print_Pow(self, expr):
        # Treat x**Rational(1,n) as special case
        if expr.exp.is_Rational and abs(expr.exp.p) == 1 and expr.exp.q != 1:
            base = self._print(expr.base)
            expq = expr.exp.q

            if expq == 2:
                tex = r"\sqrt{%s}" % base
            elif self._settings['itex']:
                tex = r"\root{%d}{%s}" % (expq, base)
            else:
                tex = r"\sqrt[%d]{%s}" % (expq, base)

            if expr.exp.is_negative:
                return r"\frac{1}{%s}" % tex
            else:
                return tex
        elif self._settings['fold_frac_powers'] \
            and expr.exp.is_Rational \
                and expr.exp.q != 1:
            base, p, q = self._print(expr.base), expr.exp.p, expr.exp.q
            if expr.base.is_Function:
                return self._print(expr.base, "%s/%s" % (p, q))
            if self._needs_brackets(expr.base):
                return r"\left(%s\right)^{%s/%s}" % (base, p, q)
            return r"%s^{%s/%s}" % (base, p, q)
        elif expr.exp.is_Rational and expr.exp.is_negative and expr.base.is_commutative:
            # Things like 1/x
            return self._print_Mul(expr)
        else:
            if expr.base.is_Function and not isinstance(expr.base, _AppliedUndef):
                return self._print(expr.base, self._print(expr.exp))
            else:
                if expr.is_commutative and expr.exp == -1:
                    #solves issue 1030
                    #As Mul always simplify 1/x to x**-1
                    #The objective is achieved with this hack
                    #first we get the latex for -1 * expr,
                    #which is a Mul expression
                    tex = self._print(S.NegativeOne * expr).strip()
                    #the result comes with a minus and a space, so we remove
                    if tex[:1] == "-":
                        return tex[1:].strip()
                if self._needs_brackets(expr.base):
                    tex = r"\left(%s\right)^{%s}"
                else:
                    tex = r"%s^{%s}"

                return tex % (self._print(expr.base),
                              self._print(expr.exp))

# Different math namespace python printer
_python_code_printer = {"":_CustomPythonCodePrinter("", ),
                        "np":_CustomPythonCodePrinter("np"),
                        "numpy":_CustomPythonCodePrinter("numpy"),
                        "math":_CustomPythonCodePrinter("math"),
                        "ufl":_CustomPythonCodePrinter("ufl"),}

# FIXME: What on earth is ordered used for?!?
_ccode_printer = _CustomCCodePrinter(order=_order)
_cppcode_printer = _CustomCCodePrinter(cpp=True, order=_order)
_ccode_float_printer = _CustomCCodePrinter(float_precision="single", order=_order)
_cppcode_float_printer = _CustomCCodePrinter(cpp=True, float_precision="single", order=_order)
_sympy_printer = _CustomPythonPrinter()
_matlab_printer = _CustomMatlabCodePrinter(order=_order)

def ccode(expr, assign_to=None):
    """
    Return a C-code representation of a sympy expression
    """
    ret = _ccode_printer.doprint(expr)
    if assign_to is None:
        return ret
    return "{0} = {1}".format(assign_to, ret)

def cppcode(expr, assign_to=None, float_precision="double"):
    """
    Return a C++-code representation of a sympy expression
    """
    if float_precision == "double":
        ret = _cppcode_printer.doprint(expr)
    else:
        ret = _cppcode_float_printer.doprint(expr)
        
    if assign_to is None:
        return ret
    return "{0} = {1}".format(assign_to, ret)

def pythoncode(expr, assign_to=None, namespace="math"):
    """
    Return a Python-code representation of a sympy expression
    """
    ret = _python_code_printer[namespace].doprint(expr)
    if assign_to is None:
        return ret
    return "{0} = {1}".format(assign_to, ret)

def sympycode(expr, assign_to=None):
    ret = _sympy_printer.doprint(expr)
    if assign_to is None:
        return ret
    return "{0} = {1}".format(assign_to, ret)
    

def matlabcode(expr, assign_to=None):
    ret = _matlab_printer.doprint(expr)
    if assign_to is None:
        return ret
    return "{0} = {1}".format(assign_to, ret)

def ccode(expr, assign_to=None, float_precision="double"):
    """
    Return a C-code representation of a sympy expression
    """
    if float_precision == "double":
        ret = _ccode_printer.doprint(expr)
    else:
        ret = _ccode_float_printer.doprint(expr)
    if assign_to is None:
        return ret
    if assign_to == "I":
        assign_to = "I_"
    return "{0} = {1}".format(assign_to, ret)

def latex(expr, **settings):
    settings["order"] = "none"
    if isinstance(expr, str):
        if expr in sp.__dict__:
            return expr
        else:
            expr = sp.sympify(expr)
    elif isinstance(expr, _scalars):
        expr = sp.sympify(expr)
        
    return _CustomLatexPrinter(settings).doprint(expr)

latex.__doc__ = _sympy_latex.__doc__

octavecode = matlabcode

__all__ = [_name for _name in globals().keys() if _name[0] != "_"]
