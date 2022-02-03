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

# Use truediv
from __future__ import division

# System imports
import types
import sympy as sp
import re

from sympy.core import relational as _relational
from sympy.core.function import AppliedUndef as _AppliedUndef

# Local imports
from utils import check_arg, deprecated
from logger import warning, error, value_error, type_error

# Patch Sympy
_AppliedUndef.is_real = True
_AppliedUndef.is_imaginary = False
_AppliedUndef.is_commutative = True
_AppliedUndef.is_hermitian = True

# Check sympy version
from distutils.version import StrictVersion
if StrictVersion(sp.__version__) < StrictVersion('0.7.5'):
    raise ImportError("model parameters requires sympy version 0.7.5 or higher.")

def Conditional(cond, true_value, false_value):
    """
    Declares a conditional

    Arguments
    ---------
    cond : A conditional
        The conditional which should be evaluated
    true_value : Any model expression
        Model expression for a true evaluation of the conditional
    false_value : Any model expression
        Model expression for a false evaluation of the conditional
    """
    cond = sp.sympify(cond)

    from sympy.core.relational import Equality, Relational
    from sympy.logic.boolalg import Boolean

    # If the conditional is a bool it is already evaluated
    if isinstance(cond, bool):
        return true_value if cond else false_value

    if not isinstance(cond, (Relational, Boolean)):
        raise type_error("Cond %s is of type %s, but must be a Relational" \
                         " or Boolean." % (cond, type(cond)))

    return sp.functions.Piecewise((true_value, cond), (false_value, sp.sympify(True)),
                                  evaluate=True)

def ContinuousConditional(cond, true_value, false_value, sigma=1.0):
    """
    Declares a continuous conditional. Instead of a either or result the
    true and false values are weighted with a sigmoidal function which
    either evaluates to 0 or 1 instead of the true or false. 

    Arguments
    ---------
    cond : An InEquality conditional
        An InEquality conditional which should be evaluated
    true_value : Any model expression
        Model expression for a true evaluation of the conditional
    false_value : Any model expression
        Model expression for a false evaluation of the conditional
    sigma : float (optional)
        Determines the sharpness of the sigmoidal function
    """
    
    cond = sp.sympify(cond)
    if not(hasattr(cond, "is_Relational") or hasattr(cond, "is_relational")):
        type_error("Expected sympy object to have is_{r,R}elational "\
                   "attribute.")
    
    if (hasattr(cond, "is_Relational") and not cond.is_Relational) or \
           (hasattr(cond, "is_relational") and not cond.is_relational):
        type_error("Expected a Relational as first argument.")
    
    # FIXME: Use the rel_op for check, as some changes has been applied
    # FIXME: in latest sympy making comparision difficult
    if "<" not in cond.rel_op and ">" not in cond.rel_op:
        type_error("Expected a lesser or greater than relational for "\
                   "a continuous conditional .")
    
    # Create Heaviside
    H = 1/(1 + sp.exp((cond.args[0]-cond.args[1])/sigma))

    # Desides which should be weighted with 1 and 0
    if ">" in cond.rel_op:
        return true_value*(1-H) + false_value*H

    return true_value*H + false_value*(1-H)
    
# Collect all parameters
_all_symbol_parameters = {}

_indexed_format = re.compile("\A([a-zA-Z]\w*)\[([\d,]+)\]\Z")

def store_symbol_parameter(param):
    """
    Store a symbol parameter
    """
    from codegeneration import sympycode
    from parameters import ScalarParam
    check_arg(param, ScalarParam)
    sym = param.sym
    #if str(sym) in _all_symbol_parameters:
    #    warning("Parameter with symbol name '%s' already "\
    #            "excist" % sym)

    param_str = sympycode(sym)
    indexed = re.search(_indexed_format, param_str)
    if indexed:
        name, indices = indexed.groups()

        # Get dict
        param_dict = _all_symbol_parameters.get(name)
        if param_dict is None:
            param_dict = {}
            _all_symbol_parameters[name] = param_dict

        param_dict[eval("({0})".format(indices))] = param
        
    else:
        _all_symbol_parameters[param_str] = param

@deprecated
def symbol_to_params(sym):
    return symbol_to_param(sym)

def symbol_to_param(sym):
    """
    Take a symbol or expression of symbols and returns the corresponding
    Parameters
    """
    from sympy.core.function import AppliedUndef
    from codegeneration import sympycode

    if sp is None:
        error("sympy is needed for symbol_to_params to work.")
        
    check_arg(sym, (sp.Symbol, AppliedUndef, sp.Derivative),
              context=symbol_to_param)
    
    param_str = sympycode(sym)
    indexed = re.search(_indexed_format, param_str)
    if indexed:
        name, indices = indexed.groups()

        # Get dict
        param = _all_symbol_parameters.get(name)
        if param is not None:
            param = param.get(eval("({0})".format(indices)))
    else:
            
        param = _all_symbol_parameters.get(sympycode(sym))

    if param is None:
        value_error("No parameter with name '{0}' "\
                    "registered. Remember to declare Params which should be "\
                    "used in expression with names.".format(sympycode(sym)))
    return param

def symbols_from_expr(expr, include_numbers=False, include_derivatives=False):
    """
    Returns a set of all symbols of an expression

    Arguments:
    ----------
    expr : sympy expression
        A sympy expression containing sympy.Symbols or sympy.AppliedUndef
        functions.
    include_numbers : bool
        If True numbers will also be returned
    include_derivatives : bool
        If True derivatives will be returned instead of its variables
    """
    from sympy.core.function import AppliedUndef

    symbols = set()
    
    pt = sp.preorder_traversal(expr)
    
    for node in pt:
        
        # Do not traverse AppliedUndef
        if isinstance(node, AppliedUndef):
            pt.skip()
            symbols.add(node)
        
        elif isinstance(node, sp.Symbol) and not isinstance(node, sp.Dummy) \
                 and node.name:
            symbols.add(node)

        elif include_numbers and isinstance(node, sp.Number):
            symbols.add(node)

        elif include_derivatives and isinstance(node, sp.Derivative):
            # Do not traverse Derivative
            pt.skip()
            symbols.add(node)
            
    return symbols

@deprecated
def iter_symbol_params_from_expr(expr):
    """
    Return an iterator over sp.Symbols from expr
    """
    check_arg(expr, sp.Basic)
    
    # Filter out dummy symbols
    return (atom for atom in expr.atoms() if isinstance(atom, sp.Symbol) \
            and not isinstance(atom, sp.Dummy) and atom.name)

@deprecated
def symbol_params_from_expr(expr):
    """
    Return a list of Symbols from expr
    """
    return [sym for sym in iter_symbol_params_from_expr(expr)]

@deprecated
def symbol_param_value_namespace(expr):
    """
    Create a value name space for the included symbols in the expression
    """
    check_arg(expr, sp.Basic)
    return dict((str(symbol_param), symbol_to_param(symbol_param).value) \
                for symbol_param in iter_symbol_params_from_expr(expr))

def value_namespace(expr, include_derivatives=False):
    """
    Create a value name space for the included symbols in the expression
    """
    from codegeneration import sympycode
    check_arg(expr, sp.Basic)
    ns = {}
    for sym in symbols_from_expr(expr, \
                        include_derivatives=include_derivatives):

        # Get value
        value = symbol_to_param(sym).value

        # Check for indexed parameters
        param_str = sympycode(sym)
        indexed = re.search(_indexed_format, param_str)
        if indexed:
            name, indices = indexed.groups()
            if name not in ns:
                ns[name] = {}
            ns[name][eval(indices)] = value
        else:
            ns[param_str] = value
            
    return ns
    return dict((sympycode(symbol), symbol_to_param(symbol).value) \
                for symbol in symbols_from_expr(\
                    expr, include_derivatives=include_derivatives))

def add_pair_to_subs(subs, old, new):
    """
    Add a pair of old and new symbols to subs. If a subs with old as a
    key already excist it will be removed before insertion.
    """
    check_arg(subs, list, 0)
    check_arg(old, sp.Basic, 1)
    check_arg(new, sp.Basic, 2)
    
    for ind, (old0, new0) in enumerate(subs):
        if old0 == old:
            subs.pop(ind)
            break
    subs.append((old, new))

# Create a sympy evaulation namespace
sp_namespace = {}
sp_namespace.update((name, op) for name, op in sp.functions.__dict__.items() \
                    if name[0] != "_")
sp_namespace["Conditional"] = Conditional
sp_namespace["ContinuousConditional"] = ContinuousConditional
sp_namespace.update((name, op) for name, op in _relational.__dict__.items() \
                    if name in ["Eq", "Ne", "Gt", "Ge", "Lt", "Le"])
sp_namespace.update((name, getattr(sp, name)) for name in ["And", "Or"])
sp_namespace["pi"] = sp.numbers.pi
sp_namespace["E"] = sp.numbers.E

sp_namespace["one"] = sp.sympify(1)
sp_namespace["two"] = sp.sympify(2)
sp_namespace["three"] = sp.sympify(3)
sp_namespace["four"] = sp.sympify(4)
sp_namespace["five"] = sp.sympify(5)
sp_namespace["ten"] = sp.sympify(10)

__all__ = [_name for _name in globals().keys() if _name[0] != "_"]

