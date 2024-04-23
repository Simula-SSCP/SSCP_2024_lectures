#!/usr/bin/env python

"""
.. _single-cell-EP-tutorial:

To run the experiments of this tutorial change directories as follows:

.. code-block:: bash

   cd ${TUTORIALS}/01_EP_single_cell/01_basic_bench 
   
Modeling EP at the cellular level
=================================

This tutorial introduces the basic steps of setting up EP simulations in an isolated myocytes.
A more detailed account on :ref:`modeling EP at the cellular scale <single-cell-EP>` is given in the manual.
For all experiments shown in this tutorial we use the single cell EP tool :ref:`bench <bench>`.
Before starting we recommend therefore to look up the basic command line options in the :ref:`bench section <bench>`
of the manual.
In this introductory tutorial we focus on simple pacing protocols
for finding a stable limit cycle. 
We model an isolated myocyte which we stimulate using an electrode for intracellular current injection.
The setup is shown in :numref:`fig-single-cell-EP`.

.. _fig-single-cell-EP:

.. figure:: /images/01_01_MyocyteEP_Setup.png
   :width: 50%
   :align: center

   Setup for single cell EP experiments. The myocyted is activated with a suprathreshold 
   stimulus current to initiate action potentials at a pacing cycle lenght of 500 ms.


.. _limit-cycle-tutorial-exposed-params:

Experimental Parameters
-----------------------

The following parameters are exposed to steer the experiment:

.. code-block:: bash

  --EP {tenTusscherPanfilov,GrandiPanditVoigt}        pick human EP model (default is tenTusscherPanfilov)

  --EP-par EP_PAR       provide a parameter modification string (default is '')

  --init INIT           pick state variable initialization file (default is none)

  --duration DURATION   pick duration of experiment (default is 500 ms)

  --bcl BCL             pick basic cycle length (default is 500 ms)

  --svRefH5 SVREFH5     pick a state variable h5 data set as reference for
                        comparison (default is none)

  --visualize           plots the myocyte action potential

  --overlays            overlays the action potential or specified variables of several
                        experiments in the same plot

  --vis_var             specified the variables that you want to visualize

Each experiment stores the state of myocyte and myofilament in the current directory in a file 
to be used as initial state vector in subsequent experiments.


.. _limit-cycle-tutorial:

Limit cycle experiments
-----------------------

Background on the computaiton of limit cycles is found in the :ref:`limit cycle <limit-cycle>` section of the manual.
Briefly, models of cellular dynamics are virtually *never* used with the values given for the initial state vector.
Rather, cells are based to a given limit cycle to approximate the experimental conditions one is interested in.
The state of the cell can be frozen at any given instant in time and this state can be reused then in subsequent simulations
as initial state vector.
In the following experiments the procedures for finding an initial state vector 
for a given model and a given basic cycle length are elucidated.
To run the experiments of this tutorial change directories as follows:

.. code-block:: bash

   cd ${TUTORIALS}/01_EP_single_cell/01_basic_bench 
   
To see all the exposed parameters itemized above in 
:ref:`experimental parameters <limit-cycle-tutorial-exposed-params>` section.

run

.. code-block:: bash

   ./run.py --help


.. _exp-ep-sc-01:

**Experiment exp01 (short pacing protocol)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We start with pacing the tenTusscherPanfilov human myocycte model at a pacing cycle length of 500 ms 
for a duration of 5 seconds (5000 msecs).       

.. code-block:: bash

   ./run.py --EP tenTusscherPanfilov --duration 5000 --bcl 500 --ID exp01 --visualize --vis_var ICaL INa IK1


You will get an overview of current traces of the model.

.. _exp-ep-sc-02:

**Experiment exp02 (limit cycle pacing protocol)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In experiment :ref:`exp01 <exp-ep-sc-01>` we observed that the state variables of the model
did not stabilize at a stable limit cycle. We increase therefore the duration of our pacing protocol
to 20 seconds (20000 msecs). 

.. code-block:: bash

   ./run.py --EP tenTusscherPanfilov --duration 20000 --bcl 500 --ID exp02 --visualize

At the end of the pacing protocol the initial state vector is saved in the file ``exp02_tenTusscherPanfilov_bcl_500_ms_dur_20000_ms.sv``.

.. code-block:: bash

   -85.1192            # Vm
   -                   # Lambda
   -                   # delLambda
   -                   # Tension
   -                   # K_e
   -                   # Na_e
   -                   # Ca_e
   0.00302465          # Iion
   -                   # tension_component
   tenTusscherPanfilov
   0.13553             # Ca_i
   3.90357             # CaSR
   0.000390854         # CaSS
   0.904553            # R_
   2.8959e-07          # O
   7.96934             # Na_i
   137.474             # K_i
   0.00176341          # M
   0.740048            # H
   0.668894            # J
   0.0173138           # Xr1
   0.469827            # Xr2
   0.0147276           # Xs
   2.47707e-08         # R
   0.999995            # S
   3.43115e-05         # D
   0.72632             # F
   0.958372            # F2
   0.995453            # FCaSS


.. _imp-param-modification-tutorial:

Ionic model parameter modification experiments
----------------------------------------------

Model behavior can be modified by providing parameter modification string through ``--imp-par``. 
Modifications strings are of the following form:

.. code-block:: bash

   param[+|-|/|*|=][+|-]###[.[###][e|E[-|+]###][\%]

where ``param`` is the name of the paramter one wants to modify 
such as, for instance, the peak conductivity of the sodium channel, ``GNa``.
Not all parameters of ionic models are exposed for modification,
but a list of those which are can be retrieved for each model using :ref:`imp-info <imp-info>`.
As an example, let's assume we are interested in specializing a generic human ventricular myocyte
based on the ten Tusscher-Panfilov model to match the cellular dynamics of myocytes
as they are found in the halo around an infract, i.e.\ in the peri-infarct zone (PZ).
In the PZ various current are downregulated. 
Patch-clamp studies of cells harvested from the peri-infract zone have reported 
a 62% reduction in peak sodium current, 69% reduction in L-type calcium current 
and a reduction of 70% and 80% in potassium currents :math:`I_{\mathrm {Kr}}` and :math:`I_{\mathrm K}`, respectively. 
In the model these modifcations are implemented by altering the peak conductivities of the respective currents as follows:

.. code-block:: bash

   # both modification strings yield the same results
   --imp-par="GNa-62%,GCaL-69%,Gkr-70%,GK1-80%"

   # or
   --imp-par="GNa*0.38,GCaL*0.31,Gkr*0.3,GK1*0.2"

In this experiment EP model parameters strings can be passed in using the ``--EP-par`` 
which expects parameter strings as input. 
The results of such modifications are illustrated in the following experiments. 


.. _exp-ep-sc-03:

**Experiment exp03 (short pacing with modified myocyte)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this experiment we modify the behavior of a tenTusscherPanfilov myocyte to match experimental observations
of myocytes harvested from peri-infarct zones in humans. 
Initially, we simulated one cycle only to observe the effect of parameter modifications
relative to the baseline tenTusscherPanfilov model. 
The referece traces are passed in and you can compared the experiment output.

.. code-block:: bash

   ./run.py --EP tenTusscherPanfilov --duration 5000 --bcl 500 --ID exp03 --EP-par "GNa-62%,GCaL-69%,Gkr-70%,GK1-80%" \
            --visualize --overlay

Make sure that the parameter modification string is correctly interpreted by :ref:`bench <bench>`
by inspecting the output log:

.. code-block:: bash

   ./run.py --EP tenTusscherPanfilov --duration 500 --bcl 5000 --ID test --EP-par "GNa-62%,GCaL-69%,Gkr-70%,GK1-80%" 


   ... 
   Ionic model: tenTusscherPanfilov
        GNa                  modifier: -62%            value: 5.63844
        GCaL                 modifier: -69%            value: 1.2338e-05
        Gkr                  modifier: -70%            value: 0.0459
        GK1                  modifier: -80%            value: 1.081
   ...

.. _exp-ep-sc-04:

**Experiment exp04 (limit cycle pacing with modified myocyte)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We repeat exp03 as a *limit cycle* experiment now by pacing for 20 seconds (20000 msecs). 
State variable and current traces stored in the baseline experiment exp02 are used as a reference.


.. code-block:: bash

   ./run.py --EP tenTusscherPanfilov --duration 20000 --bcl 500 --ID exp04 --EP-par "GNa-62%,GCaL-69%,Gkr-70%,GK1-80%" \
            --visualize --vis_var Ca_i

Visual comparison of the traces reveals that Calcium-cycling in the peri-infarct myocyte shows **alternans**.
The difference in initial state vectors between baseline and peri-infarct myocyte stored at the end of the pacing protocol
can be inspected with the *meld* or any other diff program of your choice.

.. code-block:: bash

   meld exp02_tenTusscherPanfilov_bcl_500_ms_dur_20000_ms.sv exp04_tenTusscherPanfilov_bcl_500_ms_dur_20000_ms.sv

.. figure:: /images/01_01_meld_comparison_state_vectors.png
   :align: center

   Comparing initial state vectors of baseline and peri-infarct tenTusscherPanfilov human ventricular myocyte model
   after 20 seconds of pacing at a basic cycle length of 500 ms.
"""
import os
EXAMPLE_DESCRIPTIVE_NAME = 'Basic usage of single cell tool bench - Limit cycle experiments'
EXAMPLE_AUTHOR = 'Gernot Plank <gernot.plank@medunigraz.at>'
EXAMPLE_DIR = os.path.dirname(__file__)
GUIinclude = True

import sys
import glob
import shutil
import re
import numpy as np
from carputils import settings
from carputils import tools

def visualization(args, path):
    import matplotlib.pyplot as plt
    variables = args.vis_var

    Vidx = []

    if args.overlay:
        txt_files = []
        dat_files = []
        Vidx_lst = []
        txt_legend = []
        sv_names_lst = []
        sv_data_lst = []
        directories = [x for x in os.listdir('.') if os.path.isdir(x)]

        for dir in directories:
            txt_files.append(glob.glob(os.path.join(dir, '*_trace_header.txt')))
            dat_files.append(glob.glob(os.path.join(dir, '*.dat')))
            pattern = r''+re.escape(args.EP)+ r"(.*)$"
            matches = re.search(pattern, str(dir), re.DOTALL)
            txt_legend.append(matches.group())
        for txtitem in txt_files:
            sv_names_lst.append(open(txtitem[0]).read().splitlines())
        for datitem in dat_files:
            sv_data_lst.append(np.loadtxt(datitem[0]))

        # rename state variables in-place
        for index_lst, sv_names in enumerate(sv_names_lst):
            for index, item in enumerate(sv_names):
                n_item = item.replace("sv->", "")
                sv_names[index] = n_item

                # shall this item be plot?
                if n_item in variables:
                    Vidx.append(index)

            sv_names_lst[index_lst] = sv_names
            Vidx_lst.append(Vidx)


        fig, axes = plt.subplots(1, len(Vidx_lst), sharex=True, sharey=False)
        axes = [axes] # for the case just one dataset was found, we need to make it iterable by making it a list
        idx = 0
        for i, ax in enumerate(axes):
            for j in range(0, len(Vidx_lst)):
                ax.plot(sv_data_lst[j][:, 0], sv_data_lst[j][:, Vidx[idx]+1])
                ax.set_title(sv_names_lst[0][Vidx[i]])
                ax.set_xlabel('Time (ms)')
            idx += 1
        plt.legend(txt_legend)
        plt.show()

    else:
        # no overlay
        txt_files = glob.glob(os.path.join(path, '*_trace_header.txt'))
        dat_files = glob.glob(os.path.join(path, '*.dat'))
        sv_names = open(txt_files[0]).read().splitlines()
        sv_data = np.loadtxt(dat_files[0])

        # rename state variables in-place
        for index, item in enumerate(sv_names):
            n_item = item.replace("sv->", "")
            sv_names[index] = n_item

            # shall this item be plot?
            if n_item in variables:
                Vidx.append(index)

        if len(Vidx) > 1:
            fig, axes = plt.subplots(1, len(Vidx), sharex = True, sharey = False)

            for i, ax in enumerate(axes.flatten()):
                ax.plot(sv_data[:,0], sv_data[:, Vidx[i]+1])
                ax.set_title(sv_names[Vidx[i]])
                ax.set_xlabel('Time (ms)')
            plt.show()
        else:
            plt.plot(sv_data[:,0], sv_data[:, Vidx[0]+1])
            plt.xlabel('Time (ms)')
            plt.title(sv_names[Vidx[0]])
            plt.legend([args.EP+args.EP_par+args.plug_in+args.plug_par])
            plt.grid(True)
            plt.show()
    return


def parser():

    parser = tools.standard_parser()
    group = parser.add_argument_group('experiment specific options')
    group.add_argument('--EP',
                        default = 'tenTusscherPanfilov',
                        choices = ['tenTusscherPanfilov','DrouhardRoberge', 'OHara'],
                        help = 'pick human EP model (default is tenTusscherPanfilov)')
    group.add_argument('--EP_par',
                        default = '',
                        help = 'provide a parameter modification string (default is \'\')')
    group.add_argument('--init',
                        default = '',
                        help = 'pick state variable initialization file (default is none)')
    group.add_argument('--duration', default='500',
                        help = 'pick duration of experiment (default is 500 ms)')
    group.add_argument('--bcl',
                        default='500',
                        help = 'pick basic cycle length (default is 500 ms)')
    #--------------------------------------------------------------------------
    group.add_argument('--plug_in',
                        default = '',
                        help = 'plug_in to be addedto base ionic model.')
    group.add_argument('--plug_par',
                        default = '',
                        help = 'parameter to modified in plug-in.')
    #--------------------------------------------------------------------------
    group.add_argument('--overlay',
                        action = 'store_true',
                        help = 'Overlays all existing experiments. ')
    group.add_argument('--vis_var',
                       default = 'V',
                       type = str,
                       nargs = '+',
                       help = 'Variable(s) to visualize, if empty Vm will be plotted.\n'
                              'Separate multiple variables with spaces.')
    #--------------------------------------------------------------------------
    return parser


# define job ID
def jobID(args):
    """
    Generate name of top level output directory.
    """
    tpl = 'exp_{}{}_{}{}_bcl_{}_ms_duration_{}_ms'
    return tpl.format(args.EP,args.EP_par,args.plug_in,args.plug_par, args.bcl, args.duration)
   

"""# prepare launching of visualization
def launchLimpetGUI(args,job):

    # build hdf5 state variable file
    svTracesHeader = '{}/{}_header.txt'.format(job.ID,args.EP)
    svTracesH5     = '{}_{}_traces.h5'.format(job.ID,args.EP)

    # create whitelist
    whitelist = []
    if args.svfilter == True:
        wlfilter  = 'filter_{}.txt'.format(args.EP)
        toks      = np.loadtxt(wlfilter,dtype=str)
        toklist   = toks.tolist()
        whitelist = ['--whitelist'] + toklist

    h5svcmd = [settings.execs.sv2h5b, svTracesHeader, svTracesH5 ] + whitelist
   
    job.bash(h5svcmd)

    # build hdf5 currents file
    curTracesHeader = '{}_trace_header.txt'.format(args.EP)
    curTracesH5     = '{}_{}_current_traces.h5'.format(job.ID,args.EP)

    h5curcmd = [settings.execs.sv2h5t, curTracesHeader, 'Trace_0.dat', curTracesH5 ] + whitelist
   
    job.bash(h5curcmd)

    # limpetGUI state variable visualization command
    svvcmd  = [settings.execs.limpetgui, svTracesH5]

    # GUI adjustments, only for qwt version
    GUIsettings = ['--vspacing=20',
                '--hspacing=20' ]

    #vcmd += GUIsettings

    # do we have a reference trace to compare against?
    if args.svRefH5 != '':
        svvcmd += [args.svRefH5]

    job.bash(svvcmd)

    # we want to see current traces as well?
    if args.showCurrents:
        cvcmd = [settings.execs.limpetgui, curTracesH5]

        # do we have a reference trace to compare against?
        if args.curRefH5 != '':
            cvcmd += [args.curRefH5]

    job.bash(cvcmd)
"""

def visualization_GUI(args,job):    
    # build hdf5 state variable file
    svTracesHeader = '{}/{}_header.txt'.format(job.ID,args.EP)
    svTracesH5     = '{}_{}_traces.h5'.format(job.ID,args.EP)
    h5svcmd = [settings.execs.sv2h5b, svTracesHeader, svTracesH5 ] 
   
    job.bash(h5svcmd)

    # build hdf5 currents file
    curTracesHeader = '{}/{}_trace_header.txt'.format(job.ID,args.EP)
    curTracesH5     = '{}_{}_current_traces.h5'.format(job.ID,args.EP)
    Trace0          = '{}/Trace_0.dat'.format(job.ID)

    h5curcmd = [settings.execs.sv2h5t, curTracesHeader, Trace0, curTracesH5 ] 
   
    job.bash(h5curcmd)


@tools.carpexample(parser, jobID, clean_pattern='exp*')
def run(args, job):

    # run bench with available ionic models
    cmd  = ['--duration', args.duration,
            '--stim-assign', 'on']

    # be careful here
    # stimulus current assignment to an ion species is only possible if
    # + the ion species is present
    # + and we use the "correct" name (my be inspected in the .model file)
    if args.EP == 'MBRDR':
        pass
    elif args.EP in ['tenTusscherPanfilov', 'ORd']:
        cmd += ['--stim-species', 'K_i']
    # -------------------------------------------------------------------------

    # configure EP model
    cmd += ['--imp={}'.format(args.EP)]

    if args.EP_par is not '':
        cmd += ['--imp-par', args.EP_par]


    # setup stimulus
    cmd += ['--stim-curr', 30.0,
            '--numstim', int(float(args.duration)/float(args.bcl)+1),
            '--bcl', args.bcl ]

    # numerical settings
    cmd += ['--dt', 10.0e-3]

    # IO and state management
    expID = '{}_'.format(job.ID)
    if args.ID != '':
        expID = '{}_'.format(args.ID)

    cmd += ['--dt-out', 0.1,
            '--save-ini-file', '{}{}_bcl_{}_ms_dur_{}_ms.sv'.format(expID, args.EP, args.bcl, args.duration),
            '--save-ini-time', args.duration ]

    # use steady state initialization vectors
    if args.init != '':
        if not os.path.isfile(args.init):
            print ('State variable initialization file {} not found!'.format(args.init))
            sys.exit(-1)
 
        cmd += ['--read-ini-file', args.init]

    #if args.visualize and not settings.platform.BATCH:
        #cmd += ['--validate']


    # Output options
    cmd += ['--fout={}'.format(os.path.join(job.ID, args.EP)),
            '--bin', '-v']

    job.bench(cmd, msg='Testing {}'.format(args.EP))

    # move results to folder with job.ID name
    for file in glob.glob(r'*.txt'):
        shutil.move(file, job.ID)
    for file in glob.glob(r'*.dat'):
        shutil.move(file, job.ID)
    for file in glob.glob(r'*.sv'):
        shutil.move(file, job.ID)

    # Do visualization
    if args.visualize and not settings.platform.BATCH:   
        # detailed visualization of all relevant traces
        if not args.dry:
            #launchLimpetGUI(args,job)
            if args.webGUI:

                visualization_GUI(args,job)
            else:
                visualization(args,job.ID)


if __name__ == '__main__':
    run()
