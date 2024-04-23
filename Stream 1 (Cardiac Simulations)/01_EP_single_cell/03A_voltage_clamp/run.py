#!/usr/bin/env python

r"""
This example explains the basic usage of bench for performing voltage clamp experiments (example incomplete!)  

.. _fig-01-03-voltage_clamp:

.. figure:: /images/01_03_voltage_clamp.png
    :align: center
    :width: 100%

    The voltage clamp protocol on the left generates the :math:`I_{Kr}` response on the right.

Basic usage
===========

To run the experiments of this tutorial change directories as follows:

.. code-block:: bash

   cd ${TUTORIALS}/01_EP_single_cell/03A_voltage_clamp


.. code-block:: bash

   # run clamp experiment
   bench --imp tenTusscherPanfilov  --clamp -40.0 --clamp-dur 200 --clamp-start 10  --validate --duration 500 --stim-curr 0. --fout=./VmClamp

   # convert to hdf5 for limpetGUI visualization
   bin2h5.py VmClamp_header.txt svclamp.h5
   txt2h5.py tenTusscherPanfilov_trace_header.txt Trace_0.dat curclamp.h5

   # visualize
   limpetGUIpyQt svclamp.h5
   limpetGUIpyQt curclamp.h5

"""

EXAMPLE_DESCRIPTIVE_NAME = 'Voltage clamp experiments (incomplete)'
EXAMPLE_AUTHOR = 'Gernot Plank <gernot.plank@medunigraz.at>'
GUIinclude = False

from carputils import tools

def parser():
    """ Setup command line parser.
    """
    parser = tools.standard_parser(False)
    return parser



