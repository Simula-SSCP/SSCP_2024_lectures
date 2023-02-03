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

from subprocess import Popen, PIPE, STDOUT

__all__ = ['get_output', 'get_status_output', 'get_status_output_errors']

def get_status_output_errors(cmd, input=None, cwd=None, env=None):
    pipe = Popen(cmd, shell=True, cwd=cwd, env=env, stdout=PIPE, stderr=PIPE)

    (output, errout) = pipe.communicate(input=input)

    status = pipe.returncode

    return (status, output, errout)

def get_status_output(cmd, input=None, cwd=None, env=None):
    pipe = Popen(cmd, shell=True, cwd=cwd, env=env, stdout=PIPE, stderr=STDOUT)

    (output, errout) = pipe.communicate(input=input)
    assert not errout

    status = pipe.returncode

    return (status, output)

def get_output(cmd, input=None, cwd=None, env=None):
    return get_status_output(cmd, input, cwd, env)[1]
