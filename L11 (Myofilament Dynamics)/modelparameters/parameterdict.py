# Copyright (C) 2006-2012 Johan Hake
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

"""
Contains the ParameterDict class, useful for defining
recursive dictionaries of parameters and using attribute
syntax for later access.
"""

__all__ = ["Param", "ScalarParam", "OptionParam", "ConstParam", "ArrayParam", \
           "SlaveParam", "inf", "ParameterDict"]

# System imports
try:
    from sympytools import sp
except ImportError, e:
    sp = None

from string import ljust, rjust, center

# local imports
from parameters import *
from logger import *
from utils import check_arg,  check_kwarg, scalars, value_formatter,\
     Range, tuplewrap, integers, nptypes, inf, VALUE_JUST

KEY_JUST = ljust
PAR_PREFIX = "--"
FORMAT_CONVERTER = {int:"int", float:"float", str:"string", \
                    list:None, tuple:None, bool:"int"}

def par_cmp(obj1, obj2):
    assert(isinstance(obj1, tuple))
    assert(isinstance(obj2, tuple))
    assert(isinstance(obj1[0], str))
    assert(isinstance(obj2[0], str))
    if isinstance(obj1[1], ParameterDict) and \
           not isinstance(obj2[1], ParameterDict):
        return -1
    if not isinstance(obj1[1], ParameterDict) and \
           isinstance(obj2[1], ParameterDict):
        return 1
    return cmp(obj1[0], obj2[0])
        

class ParameterDict(dict):
    """
    A dictionary with attribute-style access, 
    that maps attribute access to the real dictionary.
    """
    __slots__ = ()
    def __new__(cls, **params):

        # Generate a sub class of ParameterDict which sets the slots.
        # This is nice so the parameters show up in IPython tab completion 
        class SubParameterDict(ParameterDict):
            __slots__ = tuple(params.keys()+["_members"])

        return dict.__new__(SubParameterDict, **params)
    
    def __init__(self, **params):
        """
        Initialize a ParameterDict
        
        Arguments
        ---------
        params : (kwargs)
            A kwargs dict of Parameters of other ParameterDicts
            
        """

        # Init the dict with the provided parameters
        self._members = sorted(set(list(dict.__dict__) + \
                                   list(ParameterDict.__dict__)))+["_members"]
        for key, value in params.items():
            if key in self._members:
                type_error("The name of a parameter cannot be "\
                           "an attribute of 'ParameterDict': %s" % key)
            if sp and isinstance(value, sp.Basic) and \
                   all(isinstance(atom, (sp.Number, sp.Symbol))
                       for atom in value.atoms()):
                params[key] = SlaveParam(value, key, name=key)
            elif isinstance(value, Param):
                if value.name == "":
                    value.name = key
            elif not isinstance(value, ParameterDict):
                params[key] = Param(value, key)

            self._members.append(key)

        # Initialize base class
        dict.__init__(self, **params)
        
    def __getstate__(self):
        return self.__dict__.items()
    
    def __setstate__(self, items):
        for key, val in items:
            self.__setattr__(key, val)
    
    def __str__(self):
        """
        Returns a nice representation of the ParameterDict
        """
        return self.format_data()
    
    def __repr__(self):
        return "ParameterDict(%s)"%(", ".join("%s=%s" %\
            (k, repr(v)) for k, v in sorted(dict.iteritems(self), par_cmp)))
    
    def __delitem__(self, key):
        type_error("ParameterDict does not support item deletion")

    def pop(self, key):
        type_error("ParameterDict does not support item removal")

    def clear(self):
        type_error("ParameterDict does not support item removal")

    def fromkeys(self, *args):
        type_error("ParameterDict does not support fromkeys")

    def __setattr__(self, key, value):

        check_arg(key, str, 0, ParameterDict.__setattr__)

        if key == "_members":
            dict.__setattr__(self, key, value)
            return

        # Check if key is a registered parameter
        if not dict.__contains__(self, key):
            error("'%s' is not an item in this ParameterDict." % key, \
                  exception=AttributeError)

        # Get the original value, used for checks
        org_value = dict.__getitem__(self, key)

        if isinstance(org_value, ParameterDict):
            type_error("cannot overwrite a ParameterDict")
        
        # Set the new value
        if isinstance(org_value, Param):
            org_value.setvalue(value)
        else:
            dict.__setitem__(self, key, value)
    
    def __getattr__(self, key):
        check_arg(key, str, 0, ParameterDict.__getattr__)

        # Fix for newer ipython
        if key in ["__dict__", "__methods__", "trait_names", "_getAttributeNames"]:
            return 
            
        if not dict.__contains__(self, key):
            error("'%s' is not an item in this ParameterDict." % key, \
                  exception=AttributeError)
        
        value = dict.__getitem__(self, key)
        
        if isinstance(value, Param):
            value = value.getvalue()
        return value
    
    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __members__(self):
        return self._members

    def iterparams(self, recurse=False):
        """
        Iterate over all Param

        Arguments
        ---------
        recurse : bool (optional)
            If True each encountered ParameterDict will be entered
            
        """
        for key, value in sorted(dict.iteritems(self), par_cmp):
            if isinstance(value, ParameterDict) and recurse:
                for new_value in value.iterparams(recurse):
                    yield new_value
            elif isinstance(value, Param):
                yield value

    def iterparameterdicts(self):
        """
        Iterate over all ParameterDicts

        Arguments
        ---------
        recurse : bool (optional)
            If True each encountered ParameterDict will also be entered
            
        """
        for key, value in sorted(dict.iteritems(self), par_cmp):
            if isinstance(value, ParameterDict):
                yield value

    # A nice string to use '\xe2\x88\x88'= \in and '\xe2\x88\x9e'= \infty
    def format_data(self, indent=None):
        """
        Make a recursive indented pretty-print string of
        self and parameter subsets.
        """
        if indent is None:
            indent = 0
        max_key_length   = 0
        max_value_length = 0
        max_length       = 15
        for key, value in dict.iteritems(self):
            if not isinstance(value, ParameterDict):
                if len(key) > max_key_length:
                    max_key_length = min(len(key), max_length)
                value_length = value.format_width() \
                               if isinstance(value, Param) \
                               else len(str(value))
                if value_length > max_value_length:
                    max_value_length = min(value_length, max_length)
        s = []
        for key, value in sorted(dict.iteritems(self), par_cmp):
            
            # If the value is a ParameterDict
            if isinstance(value, ParameterDict):
                s.append("    "*indent + "%s = {"%key)
                s.append(value.format_data(indent+1))
                s.append("    "*indent + "}")
            elif isinstance(value, Param):
                s.append("    "*indent + "%s = %s"%\
                     (KEY_JUST(key, max_key_length), \
                      value.format_data(str_length=max_value_length)))
            else:
                s.append("    "*indent + "%s = %s"%\
                     (KEY_JUST(key, max_key_length), \
                      VALUE_JUST(str(value), max_value_length)))

        return "\n".join(s)
    
    def copy(self, to_dict=False):
        """
        Make a deep copy of self, including recursive copying of parameter
        subsets.

        Arguments
        ---------
        to_dict : bool (optional)
            Return a dict with items representing the values of the
            Parameters
        """
        items = {}
        for key in dict.iterkeys(self):
            value = dict.__getitem__(self, key)

            # If the value is a ParameterDict
            if isinstance(value, ParameterDict):
                items[key] = value.copy(to_dict)
            else:
                if to_dict and isinstance(value, Param):
                    items[key] = value.getvalue()
                elif isinstance(value, SlaveParam):
                    items[key] = value
                else:
                    items[key] = eval(repr(value))
        
        # FIXME: Why is this nessesary?
        items.pop("__builtins__", None)
        
        if to_dict:
            ch = dict(**items)
        else:
            ch = ParameterDict(**items)
        return ch

    def update(self, other):
        """
        A recursive update that handles parameter subsets
        correctly unlike dict.update.
        """
        check_arg(other, dict, 0, ParameterDict.update)
        
        for key in dict.iterkeys(other):
            if key not in self:
                continue
            self_value  = self[key]
            other_value = other[key]
            if isinstance(self_value, dict):
                # Update my own subdict with others subdict
                self_value.update(other_value)
            elif isinstance(self_value, Param):
                # Set my own value to others value
                self_value.setvalue(other_value)
            else:
                self[key] = other_value

    def parse_args(self, options=None, usage=""):
        """
        Parse a list of options. use sys.argv as default

        Arguments
        ---------
        options : list of str (optional)
            List of options. By default sys.argv[1:] is used. This argument
            is mostly for debugging.
        
        """
        import optparse, sys

        # Fixing bug for unicode help output
        class OptionParser(optparse.OptionParser):
            def print_help(self, f=None):
                if f is None:
                    f = sys.stdout
                f.write(self.format_help())
        parser = OptionParser(usage = usage or "usage: %prog [options]")
        
        def callback(parent, key, value_type, sequence_type=None):
            " Return a callback function that is used to parse the argument"
            if value_type in [int, float, str, bool]:
                def par_setter(option, opt_str, value, parser):
                    " Callback function to set the parameter from the options."
                    try:
                        parent[key] = value
                        #debug("Setting parameter %s to %s"%\
                        # (opt_str.replace(PAR_PREFIX, ""), str(value)))
                    except ValueError, e:
                        value_error("Trying to set '%s' while parsing "\
                                    "command line, but %s" % (key, str(e)))

            else:
                def par_setter(option, opt_str, value, parser):
                    assert value is None
                    done = 0
                    value = []
                    rargs = parser.rargs
                    while rargs:
                        arg = rargs[0]
                        
                        # Stop if we hit an arg like "--par", i.e, PAR_PREFIX
                        if PAR_PREFIX in arg:
                            break
                        else:
                            try:
                                # Convert the value
                                item = sequence_type(arg)
                                value.append(item)
                            except  ValueError, e:
                                value_error(\
                                    "Could not convert %s to '%s', while "\
                                    "setting parameter %s; %s"%\
                                    (arg, sequence_type.__name__, key, str(e)))
                                
                            del rargs[0]
                            
                    try:
                        # Changing a list to a tuple if needed
                        parent[key] = value_type(value)
                        #debug("Setting parameter %s to %s"%\
                        #(opt_str.replace(PAR_PREFIX, ""), str(value)))
                    except ValueError, e:
                        value_error("Trying to set '%s' while parsing "\
                                    "command line, but %s" % (key, str(e)))
                
            return par_setter
        
        def add_options(parent, opt_base):
            for key, value in sorted(dict.iteritems(parent), par_cmp):
                opt_base_copy = opt_base[:]
                if opt_base != PAR_PREFIX:
                    opt_base_copy += "."
                    
                # If the value is a ParameterDict
                if isinstance(value, ParameterDict):

                    # Call the function recursively
                    add_options(value, "%s%s"%(opt_base_copy, key))
                    continue

                elif isinstance(value, Param):

                    # ConstParam, ArrayParam cannot be parsed, yet
                    if isinstance(value, (ArrayParam, ConstParam)):
                        continue
                    
                    # If the value is a Param get the value
                    actuall_value = value.getvalue()

                    # Get description
                    description = value.description

                    # Check for sequence
                    if isinstance(actuall_value, (list, tuple)):
                        # If a default length of the list or tuple is 0, 
                        # assume sequence type to be int
                        if len(actuall_value) == 0:
                            sequence_type = int
                        else:
                            # Else assume it to be equal to the first argument
                            sequence_type = type(actuall_value[0])
                    else:
                        sequence_type = None

                    # Nicely formated value
                    formated_value = value.format_data()

                # Check for available types
                if not type(actuall_value) in FORMAT_CONVERTER.keys():
                    continue

                # Add option with callback function
                parser.add_option("%s%s"%(opt_base_copy, key), \
                        action = "callback", 
                        callback = callback(\
                                parent, key, type(actuall_value), sequence_type), 
                        type = FORMAT_CONVERTER[type(actuall_value)], 
                        help = "Default(%s)%s"%(str(formated_value),\
                                        (": " + description) if description else "")
                        )
        
        # Start recursively adding options
        add_options(self, PAR_PREFIX)

        # Parse command line options
        if options:
            parser.parse_args(options)
        else:
            parser.parse_args()
            
    def optstr(self):
        """
        Return a string with option set
        
        An option string can be sent to a script using a parameter dict
        to set its parameters from command line options
        """
        def option_list(parent, opt_base):
            ret_list = []
            opt_base_copy = opt_base[:]
            if opt_base != PAR_PREFIX:
                opt_base_copy += "."
            for key, value in sorted(dict.iteritems(parent), par_cmp):
                # If the value is a ParameterDict
                if isinstance(value, ParameterDict):
                    # Call the function recursively
                    ret_list.extend(\
                        option_list(value, "%s%s"%(opt_base_copy, key)))
                elif isinstance(value, Param):
                    if isinstance(value, (ConstParam, SlaveParam)):
                        continue
                    # If the value is a Param get the value
                    value = value.getvalue()
                    
                # Check for available types
                if not type(value) in FORMAT_CONVERTER.keys():
                    continue

                ret_list.append("%s%s"%(opt_base_copy, key))
                if type(value) in [list, tuple]:
                    for item in value:
                        ret_list.append(str(item))
                else:
                    value = int(value) if isinstance(value, bool) else value
                    ret_list.append(str(value))
                        
            return ret_list
        
        return " " + " ".join(option_list(self, PAR_PREFIX))
