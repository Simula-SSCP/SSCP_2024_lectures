#!/usr/bin/env python

r"""
.. _tutorial_single-cell-APD-restitution:

This tutorial demonstrates how to compute action potential duration (APD) restitution in a single cardiac cell.

To run the experiments of this tutorial change directories as follows:

.. code-block:: bash

   cd ${TUTORIALS}/01_EP_single_cell/02B_APD_restitution

Introduction
============

APD restitution is an important property of cardiac tissue. As pacing frequency is increased, APD shortens to maintain a one to one stimulus to response.  For
this tutorial, the user will be shown how to construct APD restitution curves to describe the repolarization properties of cardiac cells in response to various
pacing protocols. For details see the  APD restitution section in the manual.

Problem setup
=============

Single-cell models
------------------

This tutorial uses the cardiac cell models in openCARP's LIMPET library and the single-cell tool :ref:`bench <bench>`.
The single-cell model is a user input. To see a list of all available models, please type the following command.

.. code-block:: bash

         bench --list-imps

Restitution protocols
---------------------

Single-cell models are paced with 2-ms-long stimuli at twice capture amplitude with all restitution protocols.
Restitutions protocols are designed to reveal different features of AP restitution.
The **S1S2 protocol** illustrated in :numref:`fig-apd-restitutions-S1S2-protocol` is used to gauge the propensity
towards developing an arrhythmia.
The **dynamic protocol** rather reflects restitution for slower transitions between BCLs.
For an S1S2 pacing protocol, the user sets the basic cycle length (BCL) and number of beats, ``nbeats``, for the S1 pacing. 
Following S1 pacing, a single S2 beat is applied at a range of coupling intervals (CI) chosen by the user.
The basics of the S1S2 protocol are illustrated in :numref:`fig-apd-restitutions-S1S2-protocol`.

.. _fig-apd-restitutions-S1S2-protocol:

.. figure:: /images/01_02B_restitution_S1S2.png
    :align: center
    :width: 100%

    Illustration of the S1-S2 pacing protocol: During an initial pre-pacing period where a number of ``prebeats`` stimuli are delivered
    at the chosen ``BCL``, the action potential is stabilized.
    Alternatively, a snapshot of an AP stabilized at the given BCL can be used and read in using ``--initial``.
    After stabilization ``BCL`` is kept constant, but prematurity of the CI of the S2 is increased
    by decrementing the CI from the starting CI (``CI1``) (chosen in this experiment to be CI = ``CI1`` = ``BCL``)
    with decrements of ``CIinc`` down to the final S2 CI of ``CI0``.


When using a dynamic pacing protocol, the S1 cycle length is decremented sequentially and continuously after a user chosen number of beats, ``nbeats`` 
until the minimum CI of ``CI0`` is reached. The protocol is graphically illustrated in :numref:`fig-apd_restitutions-dynamic-protocol`.

.. _fig-apd_restitutions-dynamic-protocol:

.. figure:: /images/01_02B_restitution_dynamic.png
   :align: center
   :width: 100%

   Illustration of the dynamic restitution protocol: Pacing (again after some prepacing phase or restarting from a stabilized checkpoint for a given BCL)
   starts with a train of ``nbeats`` stimuli at the longest CI of ``CI1``. 
   CI is decremented by ``CIinc`` after each pulse train until the minimum CI of ``CI0`` is reached.

Action potential duration 
-------------------------

Activation potential duration is computed as the time it takes to reach 90% repolarization (:math:`APD_{90}`) from the maximum action potential upstroke potential.

Usage
=====

The following optional arguments are available (default values are indicated):

.. code-block:: bash

  ./run.py --help 
    --Protocol          Default: S1S2
                        Restitution protocol, either S1S2 or Dynamic
    --prebeats          Default: 20
                        Number of pre-pacing beats for S1 pacing at BCL
    --inital            Initial state vector representing limit cycle for chosen BCL
    --nbeats            Default: 10
                        Number of beats for S1 pacing at BCL
    --CI0               Default: 50 ms
                        Shortest S2 coupling interval
    --CI1               Default: BCL
                        S1 cycle length and longest S2 coupling interval
    --CIinc             Default: 25 ms
                        Decrement for time interval from CI1 to CI0
    --imp               Default: tenTusscherPanfilov
                        Single-cell model to use
    --params            Default: ' '
                        Parameters of single-cell model to modify

The run.py script formats these user inputs into the following file for an S1S2 pacing protocol using bench,

.. code-block:: bash

     1             # protocol selection 1=S1S2 0=dynamic
     prebeats      # number of prepacing beats before starting protocol
     BCL           # basic cycle length
     CI1           # S2 prematurity start
     CI0           # S2 prematurity end
     nbeats        # number of beats preceding premature one
     CIinc         # decrement in S2 prematurity in ms

and the following for a dynamic pacing protocol,

.. code-block:: bash

     0             # protocol selection 1=S1S2 0=dynamic
     prebeats      # number of prepacing beats before starting protocol
     BCL           # initial basic cycle length
     CI0           # final basic cycle length
     nbeats        # number of beats per basic cycle length
     CIinc         # decrement of bcl in ms

The script run.py then feeds these user input scripts to the function --restitute in bench. The results for DI and APD are output into the ASCII file restout_APD_restitution.dat in the corresponding output directory for the given input parameters. The format of this file is described in the openCARP manual under section the describing the function --restitute in bench (3.1.2). The details of the file format are shown below.

.. code-block:: bash

     Col 1 #Beat         : Beat number of an AP
     Col 2 Prematurity   : P (premature beat) or * (no prematurity)
     Col 3 Steady State  : O (not in steady state), 1 (in steady state)
     Col 4 APD           : Action potential duration
     Col 5 DI(n)         : Diastolic interval of current beat
     Col 6 DI(n-1)       : Diastolic interval of previous beat
     Col 7 Triangulation : APD90-APD30
     Col 8 Vm_min        : Minimum potential of current beat
     Col 9 Vm_max        : Maximum potential of current beat

If run.py is ran with the ``--visualize`` option, the APD restitution curve (APD Col 4 vs. DI Col 6) in the output file will be plotted using pythons plotting functions.

Note, if the user input for CI0 is too small, you may need to trim the restout_APD_restitution.dat files after a loss of capture occurs. The visualization feature does not remove these values permanently from the output file.

Tasks
=====

To run the experiments of this tutorial change directories as follows:

.. code-block:: bash

   cd ${TUTORIALS}/01_EP_single_cell/02B_APD_restitution


1. Compare the restitution curves for two or more different ionic models. Examples are shown below.

.. code-block:: bash

  ./run.py --imp tenTusscherPanfilov --visualize

  ./run.py --imp Courtemanche --visualize

  ./run.py --imp Shannon --visualize


.. _fig-APD-restitution-tenTusscherPanfilov:

.. figure:: /images/01_02_APD_res_curves.png
   :width: 100%
   :align: center

   Differences in restitution curves tenTusscherPanfilov, Courtemanche and Shannon model

2. Using Table 2 from [Tusscher2006]_, generate a APD restitution curve for the parameter settings -params 'G_Kr=0.172,G_Ks=0.441,G_pCa=0.8666,G_pK=0.00219,G_tf=2' and compute the maximum slope of the restitution curve. It should be well above 1.0 and look similar to Figure 5 in the Tusscher2006 paper.

.. code-block:: bash

  ./run.py --imp tenTusscherPanfilov --params G_Kr=0.172,G_Ks=0.441,G_pCa=0.8666,G_pK=0.00219,G_tf=2 --visualize

3. Do the same as above in 2, but for the parameter settings -params 'G_Kr=0.134,G_Ks=0.270,G_pCa=0.0619,G_pK=0.0730,G_tf=0.6'. The maximum slope of the restitution curve should be well below 1.0, which promotes alternans and arrhythmogenesis.
 
.. code-block:: bash

  ./run.py --imp tenTusscherPanfilov --params G_Kr=0.134,G_Ks=0.270,G_pCa=0.0619,G_pK=0.0730,G_tf=0.6 --visualize

Notes: 

1. It could be useful in the future for Gernot to modify the --restitute option to determine CI0 internally rather than having the user determine it. 

2. An adaptive decrement for S2 would be useful to better define the slope of the APD restitution curve. For example, it is small when APD does not change much to the next decrement, and is increased when APD does change above a certain threshold. 

3. It would also maybe be useful to print out the Vm for each S1S2 coupling interval to better visualize the restitution behavior. The run.py currently uses the option --res-trace to output restout.txt, but the Vm in the file format is not well described in the carpmanual or bench documentation.

4. Lastly, you may need to adjust CI0 and CI1 to the bounds at which the chosen single-cell model was constrained to. The best thing to do is find an APD restitution protocol in the published manuscript for the model, then try to reproduce it.

.. rubric:: References

.. [Tusscher2006] ten Tusscher KHWJ, Panfilov AV. 
                 **Alternans and spiral breakup in a human ventricular tissue model.**
                 *Am J Physiol Heart Circ Physiol*, 291(3):H1088-H1100, 2006.
                 `[Pubmed] <https://www.ncbi.nlm.nih.gov/pubmed/16565318>`_

"""

import os
EXAMPLE_DESCRIPTIVE_NAME = 'Single-cell APD restitution'
EXAMPLE_AUTHOR = 'Jason Bayer <jason.bayer@ihu-liryc.fr>'
EXAMPLE_DIR = os.path.dirname(__file__)
GUIinclude = True

from datetime import date
from carputils import settings
from carputils import tools
from matplotlib import pyplot
import numpy as np

def parser():
    # Generate the standard command line parser
    parser = tools.standard_parser()
    group  = parser.add_argument_group('experiment specific options')
    # Add arguments    
    group.add_argument('--Protocol',
                        default = 'S1S2',
                        choices  =['S1S2', 'Dynamic'],
                        help = 'Pacing protocol for restitution curve')
    group.add_argument('--prebeats',
                        type = int,
                        default = 20,
                        help='Number of pre-pacing beats at chosen pacing cycle length PCL')
    group.add_argument('--initial',
                        default = None,
                        help = 'Initialize with a stabilized limit cycle state vector precomputed for the chosen PCL')
    group.add_argument('--nbeats',
                        type = int,
                        default = 5,
                        help = 'Number of beats for S1 pacing at CI1')
    group.add_argument('--BCL',
                        type = int,
                        default = 600,
                        help = 'Reference basic cycle length')
    group.add_argument('--CI0',
                        type  =int,
                        default = 50,
                        help = 'Shortest coupling interval (default: 50 ms)')
    group.add_argument('--CI1',
                        type = int,
                        help = 'Longest coupling interval (default: PCL)')
    group.add_argument('--CIinc',
                        type = int,
                        default = 25,
                        help = 'Decrement for coupling interval (default: 25 ms)')
    group.add_argument('--imp',
                        default = 'tenTusscherPanfilov',
                        help =  'Ionic model')
    group.add_argument('--params',
                        default = None,
                        help = 'Ionic model parameters')

    return parser

def plotResults(di,apd,xmin,xmax,ymin,ymax,webgui,idExp):
    if (webgui):
        datadic = {'labels':{'labelsAB':[]}, \
                'datasets':{'xlim':[xmin,xmax], 'ylim':[ymin,ymax],'labelXY':['Diastolic Interval (ms)', 'Action Potential Duration (ms)'],\
                'valueX':di, 'valueY1':apd, 'valueY2':[]}}
        
        with open(idExp + "_" + "matplotM.txt", 'w') as f:
            for key, value in datadic.items():
                for key2, value2 in value.items():
                    f.write('%s\n' % (value2))
    else:
        # Plot APD vs DI
        import matplotlib.pyplot as plt
        fig = pyplot.figure()
        ax = fig.add_subplot(1,1,1)
    
        ax.plot(di, apd, 'rx-')
        
        ax.set_xlabel('Diastolic Interval (ms)')
        ax.set_ylabel('Action Potential Duration (ms)')
        ax.set_ylim(ymin,ymax)
        ax.set_xlim(xmin,xmax)
        
        pyplot.show()

def visualize(job, args):
    """
    """
    apdfile = os.path.join(job.ID, 'restout_APD_restitution.dat')
    file = open(apdfile, 'r')
    lines=file.readlines()
    di = []
    apd = []
    cnt = 0
    diffdi = 0
    diffapd = 0
    for line in lines:
        if line[0] == "#": 
            continue
        p = line.split()
        if int(cnt) > int(0):
            diffdi = float(di[int(cnt)-1])-float(p[5])
            diffapd = float(apd[int(cnt)-1])-float(p[3])
        if float(diffdi) > float(-5) and float(diffapd) > float(-10):
            apd.append(float(p[3]))
            di.append(float(p[5]))
        else:
            break
        cnt += 1
    file.close()

    print(apd)

    plotResults(di,apd,min(di)-10,max(di)+10,min(apd)-10,max(apd)+10,args.webGUI,args.ID)
#    plotResults(di,apd,0.0,args.CI1,0.0,args.CI1)

def jobID(args):
    today = date.today()
    ID = '{}_CI0-{}_CI1-{}_{}'.format(today.isoformat(), args.CI0, args.CI1, args.Protocol)
    if args.params:
        ID += '_{}'.format(args.imp,args.params)
    return ID

@tools.carpexample(parser, jobID, clean_pattern='^(\d{4}-\d{2}-\d{2})|(.txt)|(.dat)')
def run(args, job):

    # Determine the threshold for the user input parameters
    stimcurr = 0
    thresh_achieved = False
    delta_curr = 2

    # check input args
    if not args.CI1:
        args.CI1 = args.BCL

    # set up ionic model
    imp_setup = ['--imp', args.imp]
    if args.params:
        imp_setup += ['--imp-par', args.params]

    # build baseline command line
    bcmd = imp_setup

    while not thresh_achieved:
        stimcurr += delta_curr
        print('Currently applied stimulus current: {}'.format(stimcurr))

        # define protocol
        pars = ['--duration', 100.1,
                '--numstim', 1,
                '--stim-start', 1,
                '--bcl', 100,
                '--stim-curr', stimcurr,
                '--stim-dur', 2,
                '--fout={}'.format(os.path.join(job.ID, 'thresh')),
                '--save-time', 100,
                '--save-file', os.path.join(job.ID, 'thresh_save.sv')]
        
        # run threshold
        job.bench(bcmd+pars)


        # Now read in the data
        if args.dry:
            thresh_achieved = True
        else:
            vmfile = os.path.join(job.ID, 'thresh.txt')
            Vm = np.loadtxt(vmfile)
            if Vm[50,1] > -10.:     # why t=50ms?
                thresh_achieved = True

    stimcurr = stimcurr*2
    print('Chosen stimulus current: {}'.format(stimcurr))

    # Write the S1S2 restitution file
    if args.Protocol == 'S1S2':
        ropt = 'S1S2'
        if not args.dry:
            with open(os.path.join(job.ID, 'restitution_protocol.txt'), 'w') as fp:
                fp.write('  1   # protocol selection 1=S1S2 0=dynamic\n')
                fp.write('{:3d} # number of prepacing beats before starting protocol\n'.format(args.prebeats))
                fp.write('{:3d} # basic cycle length\n'.format(args.BCL))
                fp.write('{:3d} # S2 prematurity start\n'.format(args.CI1))
                fp.write('{:3d} # S2 prematurity end\n'.format(args.CI0))
                fp.write('{:3d} # number of beats preceding premature one\n'.format(args.nbeats))
                fp.write('{:3d} # decrement in S2 prematurity in ms\n'.format(args.CIinc))

    if args.Protocol == 'Dynamic' and not args.dry:
        ropt='dyn'
        if not args.dry:
            with open(os.path.join(job.ID, 'restitution_protocol.txt'), 'w') as fp:
                fp.write('  0   # protocol selection 1=S1S2 0=dynamic\n')
                fp.write('{:3d} # number of prepacing beats before starting protocol\n'.format(args.prebeats))
                fp.write('{:3d} # initial basic cycle length\n'.format(args.BCL))
                fp.write('{:3d} # final basic cycle length\n'.format(args.CI0))
                fp.write('{:3d} # number of beats preceding premature one\n'.format(args.nbeats))
                fp.write('{:3d} # decrement in S2 prematurity in ms\n'.format(args.CIinc))


    # Run bench with restitution file
    pars = ['--stim-curr', stimcurr,
            '--stim-dur', 2,
            '--restitute', ropt,
            '--res-file',  os.path.join(job.ID, 'restitution_protocol.txt'),
            '--res-trace', os.path.join(job.ID, 'restout_trace.txt'),
            '--fout={}'.format(os.path.join(job.ID, 'restout'))]

    if args.initial:
        pars += ['--initial', args.initial]

    # run threshold
    job.bench(bcmd+pars)

    #Process the data into two columns
    if args.visualize and not settings.platform.BATCH:
        visualize(job,args)
        apdfile = os.path.join(job.ID, 'restout_APD_restitution.dat')

        cmd = [settings.execs.APDRESTITUTION, apdfile, args.imp]
        job.bash(cmd)

if __name__ == '__main__':
    run()
