#!/usr/bin/env python

"""
This tutorial explains the basics of using the code generation tool ``limpet_fe.py``
for generating ODE solver code for models of cellular dynamics. The code needs to be compiled, thus you
to have a working developer environment in place (PETSc and other required libraries). The best
way to make sure this is the case and to avoid compatibility issues is to compile openCARP
from source as `outlined here 
<https://opencarp.org/download/installation#building-from-source>`_.

.. _limpet-fe-tutorial:

=====================
Usage of limpet_fe.py 
=====================


``limpet_fe.py`` is the :ref:`EasyML <EasyML>` to C translator for writing ionic models.
The easiest way to see how to write a model is to examine a simpler example. 
To work on this tutorial do

.. code-block:: bash

   cd ${TUTORIALS}/01_EP_single_cell/04_limpet_fe

-----------------
Input .model file
-----------------

Let's look at the Beeler-Reuter model (in your current folder: my_MBRDR.model) as modified by Drouhard and Roberge::
    
    Iion; .nodal(); .external();
    V; .nodal(); .external(Vm); 

    V; .lookup(-800, 800, 0.05);
    Ca_i; .lookup(0.001, 30, 0.001); .units(uM);

    V_init = -86.926861;

    # sodium current
    GNa = 15;
    ENa  = 40.0;
    I_Na = GNa*m*m*m*h*(V-ENa);
    I_Na  *= sv->j;

    a_m = ((V < 100)
           ? 0.9*(V+42.65)/(1.-exp(-0.22*(V+42.65)))
           : 890.94379*exp(.0486479163*(V-100.))/
                (1.+5.93962526*exp(.0486479163*(V-100.)))
           );
    b_m = ((V < -85)
           ? 1.437*exp(-.085*(V+39.75))
           : 100./(1.+.48640816*exp(.2597503577*(V+85.)))
           );
    a_h = ((V>-90.)
           ? 0.1*exp(-.193*(V+79.65))
           : .737097507-.1422598189*(V+90.)
           );
    b_h = 1.7/(1.+exp(-.095*(V+20.5)));

    a_d = APDshorten*(0.095*exp(-0.01*(V-5.)))/
      (exp(-0.072*(V-5.))+1.);
    b_d = APDshorten*(0.07*exp(-0.017*(V+44.)))/
      (exp(0.05*(V+44.))+1.) ;

    a_f = APDshorten*(0.012*exp(-0.008*(V+28.)))/
      (exp(0.15*(V+28.))+1.);
    b_f = APDshorten*(0.0065*exp(-0.02*(V+30.)))/
      (exp(-0.2*(V+30.))+1.);

    a_X = ((V<400.)
           ? (0.0005*exp(0.083*(V+50.)))/
           (exp(0.057*(V+50.))+1.) 
           : 151.7994692*exp(.06546786198*(V-400.))/
           (1.+1.517994692*exp(.06546786198*(V-400.)))
           );

    b_X   = (0.0013*exp(-0.06*(V+20.)))/(exp(-0.04*(V+20.))+1.);

    xti   = 0.8*(exp(0.04*(V+77.))-1.)/exp(0.04*(V+35.));

    I_K = (( V != -23. )
           ? 0.35*(4.*(exp(0.04*(V+85.))-1.)/(exp(0.08*(V+53.))+
                                                  exp(0.04*(V+53.)))-
                   0.2*(V+23.)/expm1(-0.04*(V+23.)))
           : 
           0.35*(4.*(exp(0.04*(V+85.))-1.)/(exp(0.08*(V+53.))+
                                                exp(0.04*(V+53.))) + 0.2/0.04 )
           );

    # slow inward
    Gsi = 0.09;
    Esi = -82.3-13.0287*log(Ca_i/1.e6);
    I_si = Gsi*d*f*(V-Esi);
    I_X  = X*xti;

    Iion= I_Na+I_si+I_X+I_K;

    Ca_i_init = 3.e-1;
    diff_Ca_i = ((V<200.)
                 ? (-1.e-1*I_si+0.07*1.e6*(1.e-7-Ca_i/1.e6))
                 : 0
                 );

    group {
      GNa;
      Gsi;
      APDshorten = 1;
    } .param();

    group {
      I_Na;
      I_si;
      I_X;
      I_K;
    } .trace();

Generally, it looks like C code with a few extra commands.
Let's break it down a bit::

    Iion; .nodal(); .external();
    V; .nodal(); .external(Vm); 
    
**These lines are very important.** ``.external()`` tells us that these are global variables and through these variables
we will interact with the simulation. The argument to *external()* is the actual name of the global variable if we want to call it something else locally. Here, the local variable ``V`` is actually the global variable ``Vm`` while ``Iion`` is the
global name which we use locally. To alter the transmembrane voltage, ``Iion`` must be assigned a value. openCARP then uses this value of *Iion* to adjust the transmembrane voltage.
**You do not specify the change of *Vm*.**

.. note::

    Ionic models are fully functioning models. Plugins are additional components which must be added to an ionic model. 
    They modify or expand behaviour, eg., a new channel or a force genration description.
    For an ionic model, the ionic current is set, e.g., Iion = 2.3, while plug-ins add an additional 
    current to an existing current, i.e., Iion = Iion + 2.3

The next two lines ::

    V; .lookup(-800, 800, 0.05);
    Ca_i; .lookup(0.001, 30, 0.001); .units(uM);

tell the translator to use lookup tables for variables which are functions of these variables in order to avoid expensive function calls. The table range for *V* is -100 to 100 in steps of 0.05. This should be done after the model is verified to be working correctly.

There are several Hodgkin-Huxley type gating variables. Here is the *f* gate ::

    a_f = APDshorten*(0.012*exp(-0.008*(V+28.)))/
      (exp(0.15*(V+28.))+1.);
    b_f = APDshorten*(0.0065*exp(-0.02*(V+30.)))/
      (exp(-0.2*(V+30.))+1.);

Variables of the form *a_XXX* and *b_XXX* are automatically recognized as the :math:`\\alpha` and :math:`\\beta` coefficients. The differential equation for the variable *XXX* will be automatically generated as well as an intial condition. Alternatively, one can assign *tau_XXX* and *XXX_inf*,  which correspond to  :math:`\\tau_{XXX}` and :math:`XXX_{\\inf}`.

.. note::

    if a variable is a differential variable but is **NOT** a recognized *gating* variable, its initial condition
    init_XXX must be explicitly set. 
    That is why you will find *Ca_i_init* in the .model file.

The block:: 

  group {
      GNa;
      Gsi;
      APDshorten = 1;
    } .param();

declares variables with default values. However, their values can be changed at the start of a simulation with the parameter changing syntax.

The section::

    group {
      I_Na;
      I_si;
      I_X;
      I_K;
    } .trace();

declares a group of trace variables. If a node is selected as being traced, these quantities will be output as functions of time at the node.

.. _units-easyml:

-----
Units
-----

Units are a never ending source of grief. All sorts are used in various papers. openCARP expects certain standards so that interactions are possible between components. The table below gives the recommended units

==================== ==========================
quantity             units                      
==================== ==========================
membrane current     :math:`\mu A/cm^2 = pA/pF`
dX/dt                :math:`ms^{-1}`
:math:`[Ca]_i`       :math:`\mu M`
:math:`[X]`          :math:`mM`
voltage/potential    :math:`mV`      
membrane conductance :math:`mS/cm^2`
:math:`\\tau_X`      :math:`ms`
:math:`\\alpha,\\beta` :math:`ms^{-1}`
==================== ==========================

Internally, you can use what you like but you need to convert any variables passed between openCARP and your model, i.e., the total membrane current, concentrations, derivatives, and variables associated with gates.

-----------------------
Generating the C source
-----------------------

Now, we need to make a runtime shared object library::

    make_dynamic_model.sh my_MBRDR

``make_dynamic_model.sh`` (located in ``physics/limpet/src``) calls ``limpet_fe.py`` (located in ``physics/limpet/src/python``) to convert the model file to C++ code for compilation.
Provided you have no errors, this will produce the files, *my_MBRDR.cc* and *my_MBRDR.h*.
``make_dynamic_model.sh`` will then call ``make_dynamic_model.py``,
which will produce *my_MBRDR.so*. This shared library can then be loaded by openCARP at runtime 
and provide an ionic model with the name ``my_MBRDR``.

``NOTE:`` The best way to make ensure a working development environment including thirdparty dependencies
like PETSc and to avoid compatibility issues between your openCARP binary and the newly compile model library 
is to compile openCARP from source as `outlined here 
<https://opencarp.org/download/installation#building-from-source>`_.
To create a dynamic model, you need to have compiled openCARP from its source. The script needs the path of the source code as well as compiled libraries from openCARP.

-------------
Using the IMP
-------------

Single cell
-----------

The program `bench` is used to run single cell experiments.
See :ref:`bench <single-cell-EP-tutorial>` for more details running this program.
In this tutorial, *run.py* is just a wrapper for *bench*::

   run.py --load-module ./my_MBRDR.so 

.. note::

    for the *--load* option, an absolute path must be specified. That is why we used the *"./"* in *"./my_MBRDR.so"*.
    If the *--imp* option is not specified, it will attempt 
    to load the ionic model with the same name as the loaded library.

Remembering that we set ``APDshorten`` as a parameter, we can see its effect ::

    run.py --load-module ./my_MBRDR.so --imp-par='APDshorten=3'

As an exercise, try adding ``Ca_i`` as a trace variable, or add a *j* gate to the sodium channel described by the follwing equations
    :math:`\\alpha_j = 0.055\\frac{exp(-0.25*(V+78))}{exp(-(V+78)/5)+1}` and
    :math:`\\beta_j  = \\frac{0.3}{(exp(-0.1*(V+32))+1}`

Parameter files
---------------

To use the ionic model in a tissue simulation, it is specified in the parameter file as ::

    num_external_imp = 1
    external_imp = ./my_MBRDR.so
    imp_region[0].im = my_MBRDR

Obviously, multiple IMPs can be added by increasing ``num_external_imp``. Make sure that the shared library was built in the same
environment (operating system, compiler etc.) that openCARP was built in.

"""
import os
import warnings
EXAMPLE_DESCRIPTIVE_NAME = 'Basic usage of code generation tool limpet_fe.py'
EXAMPLE_AUTHOR = 'Edward Vigmond <edward.vigmond@ubordeaux-1.fr>'
EXAMPLE_DIR = os.path.dirname(__file__)
GUIinclude = True

from datetime import date
from carputils import settings
from carputils import tools

def parser():
    parser = tools.standard_parser()
    group  = parser.add_argument_group('experiment specific options')
    group.add_argument('--load-module',
                       type = str,
                       default = 'my_MBRDR.so',
                       help = 'IMP library to link')
    group.add_argument('--imp-par',
                       type = str,
                       default = 'APDshorten=3',
                       help = 'ionic model adjustments')
    group.add_argument('--numstim',
                       type = int,
                       default = 1,
                       help = 'number of stimuli')
    group.add_argument('--bcl',
                       type = float,
                       default = 1000.,
                       help = 'pacing cycle length (ms)')
    group.add_argument('--dt',
                       type = float,
                       default = 0.025,
                       help = 'time step (ms)')
    group.add_argument('--showCurrents',
                       action = 'store_true',
                       help = 'show currents')
    group.add_argument('--curRefH5',
                       default = None,
                       help = 'compare with precomputed current')
    return parser

def jobID(args):
    """
    Generate name of top level output directory.
    """
    today = date.today()
    tpl = '{}_limpet_fe'
    return tpl.format(today.isoformat())

# prepare launching of visualization
def launchLimpetGUI(args, job, IM_MODULE):

    EP = os.path.basename(IM_MODULE.rstrip('.so'))

    # build hdf5 state variable file
    svTracesHeader = '{}_header.txt'.format(os.path.join(job.ID, EP))
    svTracesH5     = '{}_traces.h5'.format( os.path.join(job.ID, EP))

    # create whitelist
    whitelist = []
    h5svcmd   = [settings.execs.sv2h5b, svTracesHeader, svTracesH5] + whitelist
    job.bash(h5svcmd, 'Build hdf5 traces file')

    # build hdf5 currents file
    curTracesHeader = '{}_trace_header.txt'.format(EP)
    curTracesH5     = '{}_current_traces.h5'.format(os.path.join(job.ID, EP))

    h5curcmd = [settings.execs.sv2h5t, curTracesHeader, 'Trace_0.dat', curTracesH5 ] + whitelist
    job.bash(h5curcmd, 'Build hdf5 currents file')

    if not args.webGUI:

        # limpetGUI state variable visualization command
        svvcmd = [settings.execs.limpetgui, svTracesH5]
        job.bash(svvcmd, 'Lauching limpetgui')
    
        # we want to see current traces as well?
        if args.showCurrents:
            cvcmd = [settings.execs.limpetgui, curTracesH5]

            # do we have a reference trace to compare against?
            if args.curRefH5 is not None:
                cvcmd += [args.curRefH5]
            
            job.bash(cvcmd, 'Launching limpetgui')


@tools.carpexample(parser, jobID, clean_pattern='^(\d{4}-\d{2}-\d{2})|\w*.[chst]')
def run(args, job):

    # check availablity of shared object file
    if os.path.exists(args.load_module) or \
        os.path.exists(args.load_module.rstrip('.so') + '.model'):
        # user input with correct location of module file
        IM_MODULE = os.path.abspath(args.load_module)
    elif os.path.exists(os.path.join(EXAMPLE_DIR, args.load_module)) or \
         os.path.exists(os.path.join(EXAMPLE_DIR, args.load_module.rstrip('.so')+'.model')):
        # Could not find module file. Looking in tutorial folder.
        IM_MODULE = os.path.join(EXAMPLE_DIR, args.load_module)
    else:
        warnings.warn('Could not find "{}.[so,model]" anywhere! Aborting...'.format(args.load_module.rstrip('.so')))
        return

    # make sure the shared object file for ionic model library is available
    # or at least the .model file so that we can build the .so module
    if not os.path.exists(IM_MODULE):
        # let's create it
        #----------------------------------------------------------------------
        # run make_dynamic_model.sh, it will
        # call limpet_fe.py to generate the C files, and then
        # call make_dynamic_model.py to compile the shared object
        IM_MODEL_FILE = IM_MODULE.rstrip('.so') + '.model'
        cmd = [settings.execs.MAKEDYNAMICMODEL, IM_MODEL_FILE]
        job.bash(cmd, 'Compiling ionic model sources')


    # run bench with available ionic models
    EP = os.path.basename(IM_MODULE).rstrip('.so')
    cmd = ['--load-module', IM_MODULE,
           '--numstim', args.numstim,
           '--bcl', args.bcl,
           '--dt', args.dt,
           '--validate',
           '--fout={}'.format(os.path.join(job.ID, EP))]

    if args.imp_par is not None:
        cmd += ['--imp-par', args.imp_par]
    job.bench(cmd)

    # Do visualization
    if args.visualize and not settings.platform.BATCH:

        # detailed visualization of all relevant traces
        launchLimpetGUI(args, job, IM_MODULE)

if __name__ == '__main__':
    run()
