# Copyright (C) 2005-2012 Martin Sandve Alnaes and Anders Logg
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

# Modified by Johan Hake, 2009-2012.

import sys
import types
import logging
import inspect

__all__ = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "Logger"] 

# Import default log levels
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

# Base class for ModelParameters exceptions
class ModelParametersException(Exception):
    "Base class for ModelParameters exceptions"
    pass

# This is used to override emit() in StreamHandler for printing without newline
def emit(self, record):
    message = self.format(record)
    format_string = "%s" if getattr(record, "continued", False) else "%s\n"
    self.stream.write(format_string % message)
    self.flush()

# Colors
RED   = "\033[1;37;31m%s\033[0m"
BLUE  = "\033[1;37;34m%s\033[0m"
GREEN = "\033[1;37;32m%s\033[0m"

# Logger class
class Logger:

    def __init__(self, name):
        "Create logger instance."
        self._name = name

        # Set up handler
        h = logging.StreamHandler(sys.stdout)

        sys.stdout.flush()
        h.setLevel(WARNING)
        #h.setFormatter(logging.Formatter("%(levelname)s, %(name)s,
        #%(pathname)s, line %(lineno)s, in %(module)s\n    %(message)s\n"))
        
        # Override emit() in handler for indentation
        h.emit = types.MethodType(emit, h)#, h.__class__)
        self._handler = h

        # Set up logger
        self._log = logging.getLogger(name)
        assert len(self._log.handlers) == 0
        self._log.addHandler(h)
        self._log.setLevel(DEBUG)

        self._logfiles = {}

        # Set initial indentation level
        self._indent_level = 0

        # Set flag for raising errors
        self._raise_error = True

        # Setup stack with default logging level
        self._level_stack = [DEBUG]

        # Set prefix
        self._prefix = ""

        # Set default Exception
        self._DefaultException = ModelParametersException

    def set_default_exception(self, exception):
        if not issubclass(exception, Exception):
            raise TypeError("Expected a subclass of Exception")
        self._DefaultException = exception

    def add_logfile(self, filename=None, mode="a"):
        if filename is None:
            filename = "%s.log" % self._name
        if filename in self._logfiles:
            self.warning("Trying to add logfile %s multiple times." % filename)
            return
        h = logging.FileHandler(filename, mode)
        h.emit = types.MethodType(emit, h, h.__class__)
        h.setLevel(self._log.level)
        self._log.addHandler(h)
        self._logfiles[filename] = h
        return h

    def remove_logfile(self, filename):
        if filename in self._logfiles:
            h = self._logfiles.pop(filename)
            self._log.removeHandler(h)

    def set_raise_error(self, value):
        self._raise_error = bool(value)

    def get_logfile_handler(self, filename):
        return self._logfiles[filename]

    def log(self, level, *message):
        "Write a log message on given log level"
        text = self._format_raw(*message)
        if len(text) >= 3 and text[-3:] == "...":
            self._log.log(level, self._format(*message), \
                          extra={"continued": True})
        else:
            self._log.log(level, self._format(*message))

    def debug(self, *message):
        "Write debug message."
        self.log(DEBUG, *message)

    def info(self, *message):
        "Write info message."
        self.log(INFO, *message)

    def info_red(self, *message):
        "Write info message in red."
        self.log(INFO, RED % self._format_raw(*message))

    def info_green(self, *message):
        "Write info message in green."
        self.log(INFO, GREEN % self._format_raw(*message))

    def info_blue(self, *message):
        "Write info message in blue."
        self.log(INFO, BLUE % self._format_raw(*message))

    def warning(self, *message):
        "Write warning message."
        self.log(WARNING, self._format_raw(*message))

    def error(self, *message, **kwargs):
        "Write error message and raise an exception."
        self.log(ERROR, self._format_raw(*message))
        raise_error = kwargs.get("raise_error", self._raise_error)
        Exception = kwargs.get("exception", self._DefaultException)
        
        if raise_error:
            raise Exception(self._format_raw(*message))

    def type_error(self, *message, **kwargs):
        "Write error message and raise a type error exception."
        kwargs["exception"] = TypeError
        self.error(*message, **kwargs)

    def value_error(self, *message, **kwargs):
        "Write error message and raise a value error exception."
        kwargs["exception"] = ValueError
        self.error(*message, **kwargs)

    def begin_log(self, *message):
        "Begin task: write message and increase indentation level."
        self.info(*message)
        #self.info("-"*len(self._format_raw(*message)))
        self.add_log_indent()

    def end_log(self):
        "End task: write a newline and decrease indentation level."
        self.info("")
        self.add_log_indent(-1)

    def push_log_level(self, level):
        "Push a log level on the level stack."
        self._level_stack.append(level)
        self.set_log_level(level)

    def pop_log_level(self):
        """
        Pop log level from the level stack, reverting to before
        the last push_level.
        """
        self._level_stack.pop()
        level = self._level_stack[-1]
        self.set_log_level(level)

    def suppress_logging(self):
        "Suppress all logging"
        self.set_log_level(CRITICAL+1)

    def set_log_level(self, level):
        "Set log level."
        self._level_stack[-1] = level
        self._log.setLevel(level)
        self._handler.setLevel(level)
        for h in self._logfiles.values():
            h.setLevel(level)

    def get_log_level(self):
        "Get log level."
        return self._level_stack[-1]

    def set_log_indent(self, level):
        "Set indentation level."
        self._indent_level = level

    def add_log_indent(self, increment=1):
        "Add to indentation level."
        self._indent_level += increment

    def get_log_handler(self):
        "Get handler for logging."
        return self._handler

    def flush_logger(self):
        "Flush the log handler"
        for h in self._log.handlers:
            h.flush()

    def set_log_handler(self, handler):
        """
        Replace handler for logging.

        To add additional handlers instead of replacing the existing, use
        log.get_logger().addHandler(myhandler).

        See the logging module for more details.
        """
        self._log.removeHandler(self._handler)
        self._log.addHandler(handler)
        self._handler = handler
        handler.emit = types.MethodType(emit, self._handler, \
                                        self._handler.__class__)

    def get_logger(self):
        "Return message logger."
        return self._log

    def set_log_prefix(self, prefix):
        "Set prefix for log messages."
        self._prefix = prefix

    def wrap_log_message(self, message, symbol="*"):
        message = "%s %s %s"%(symbol, message, symbol)
        wrapping = symbol*len(message)
        return "\n".join(["", wrapping, message, wrapping, ""])
    
    def _format(self, *message):
        "Format message including indentation."
        indent = self._prefix + 2*self._indent_level*" "
        message = message[0] if len(message) == 1 else message[0] % message[1:]
        return "\n".join([indent + line for line in message.split("\n")])

    def _format_raw(self, *message):
        "Format message without indentation."
        message = message[0] if len(message) == 1 else message[0] % message[1:]
        return message

#--- Set up global log functions ---

_logger = Logger("ModelParameters")

for name, func in inspect.getmembers(_logger):
    if name[0] == "_":continue
    globals()[name] = func
    __all__.append(name)

