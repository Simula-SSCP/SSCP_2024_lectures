#!/usr/bin/env python

"""
======================
Converting from CellML
======================

Intro
======

CellML is a markup language for describing, amongst other things, ionic models. Many models are published and availmable from the
`CellML Model Repository <https://models.cellml.org/electrophysiology>`_. However, this format can only be processed by a machine. CARPentry uses its own MarkUp Language called :ref:`EasyML <EasyML>`.

The Script
==========

Conversion of a CellML file is performed using the ``cellml_converter.py`` script::

    usage: cellml_converter.py [-h] [--Vm VM] [--Istim ISTIM] [--out OUT]
                               [--trace-all] [--plugin] [--params]
                               [--keep-redundant]
                               CMLfile

    Convert CellML 1.0 to model format

    positional arguments:
      CMLfile           CellML file

    optional arguments:
      -h, --help        show this help message and exit
      --Vm VM           transmembrane voltage variable [V]
      --Istim ISTIM     stimulus current variable [i_Stim]
      --out OUT         output file
      --trace-all       trace all variables
      --plugin          is a plug-in, not a whole cell model
      --params          parameterize all constants
      --keep-redundant  keep redundant differential expressions, eg alpha, beta
                        and diff)


The flags mean the following

==============   ============================================================================
Flag             Meaning
==============   ============================================================================
Vm               the variable name in the CellML file referring to transmembrane voltage.
Istim            the CellML variable referring to the stimulus current. This will be removed.
out              output file which will be processed by limpet_fe.py
trace-all        add all variables to the trace so they can be monitored
plugin           not a stand alone ionic model, but a plug-in
params           make all constants modifiable as parameters
keep-redundant   keep all differential equations, even if some are not needed and redundant
==============   ============================================================================


The process of creating an :ref:`EasyML <EasyML>` file is not entirely automated. Manual intervention is always necessary. Generally, the process to create a model file is as follows:

#. *cellml_converter.py* is run on the CellML file
#. references to stimuli and extraneous variables are removed
#. redundant :ref:`gating variable equations <gate_vars>` are removed
#. :ref:`units <units-easyml>` are adjusted
#. integration methods are adjusted
#. lookup tables are implemented

.. note:: Variable names may be changed since EasyML demands global uniqueness while CellML only demands section uniqueness. Thus, in CellML, there may be two **a** variables, but in two different channels. They will be renamed to avoid the conflict in EasyML, and variables are grouped together by section after conversion.


Example 1
=========

We will begin by converting a relatively simple model, the :download:`LuoRudy II </downloads/luo_rudy_1994.cellml>`.

#. run the converter to produce the EasyML model file::

    cellml_converter.py luo_rudy_1994.cellml > luo_rudy_1994.model

#. run the model to C translator::

     limpet_fe.py luo_rudy_1994.model

   You will see the following output which has errors::

    Syntax error at line 79, token '{'
    Warning, you should only use alpha/beta OR tau/infinity while formulating gates!

    Using the tau infinity values.

    Error with d

    Warning, you should only use alpha/beta OR tau/infinity while formulating gates!

    Using the tau infinity values.

    Error with f

    Traceback (most recent call last):
    File "/home/vigmond/Software/dcse/bin/limpet_fe.py", line 1581, in <module>
        obj.printSource()
     File "/home/vigmond/Software/dcse/bin/limpet_fe.py", line 786, in printSource
        declare_type = "double ",
    File "/home/vigmond/Software/dcse/bin/limpet_fe.py", line 201, in printEquations
        for var in eqnmap.getList(target, valid):
    File "/home/vigmond/Software/dcse/LIMPET/im.py", line 220, in getList
     for d in self[sym].depend:
    File "/home/vigmond/Software/dcse/LIMPET/basic.py", line 87, in __getitem__
        return self._map[key]
    KeyError: Var("I_st")

#. Open up *luo_rudy_1994.model* in the text editor of your choice. Based on the error output, look at line **79**::

      dV_dt = ((I_st - (i_Na+i_Ca_L+i_K+i_K1+i_Kp+i_NaCa+i_p_Ca+i_Na_b+i_Ca_b+i_NaK+i_ns_Ca))/Cm); .units(mV/ms);
      I_st = ((({http://www.w3.org/1998/Math/MathML}rem:time,stimPeriod)<stimDuration) ? stimCurrent : 0.0); .units(uA/mm^2);

   It appears that *I_st* is the stimulus current which we would like to remove. We can manually remove it by deleting line 79 and
   eliminating it from line 78, or we can run ``cellml_converter.py --Istim=I_st luo_rudy_1994.cellml > luo_rudy_1994.model``

   Now we are left with errors with gating variables *d* and *f*. Locate them around line 106. Note how alpha, beta, tau and _inf are
   defined for all. By inspecting, we see that *alpha_d* and *alpha_f* are defined using the infinity and tau values so they can be removed.
   Save the file, and rerun `` limpet_fe.py luo_rudy_1994.model`` which should now have no errors.

# make the linkable library and run it to be sure::

    make_dynamic_model.sh luo_rudy_1994
    bench.debug.petsc.pt --load ./luo_rudy_1994.so

Example 2
=========

Now, we will compile the :download:`Grandi-Pasquelini-Bers model </downloads/grandi_pasqualini_bers_2010.cellml>`
which is quite complicated.

#. Run the EasyML generator::

    linux-nvs8%cellml_converter.py grandi_pasqualini_bers_2010.cellml > grandi_pasqualini_bers_2010.model
    WARNING: stimulus current not found
    WARNING: transmembrane voltage not found

   So, not ev ery author uses the same names for the same quantities. Inspecting the model file, we can see
   that transmembrane voltage is called *V_m* and the stimulating current is *I_app*. Rerun the converter::

      cellml_converter.py --Vm=V_m --Istim=I_app  grandi_pasqualini_bers_2010.cellml > grandi_pasqualini_bers_2010.model

   Generate the C code::

      limpet_fe.py grandi_pasqualini_bers_2010.model

   which does not complain but when we try to run the model ::

     bench.debug.petsc.pt --load ./grandi_pasqualini_bers_2010.so

   we get NaNs which is not good. So, at this point we need to rely on intuition and a good debugger. First we reduce the time
   step and hope it is just an integration issue with stiff equations::

     bench.debug.petsc.pt --load ./grandi_pasqualini_bers_2010.so --dt=0.005

   which luckily works. We do not want to be restricted to a 5 microsecond timestep so we need to investigate further.
   The most common issues are

   #. calcium is released explosively during the upstroke so we often need to proper integrate calcium related variables as a group with a more complicated method.
   #. gating variables are not defined with alpha/beta or tau/_inf so they can go out of bounds, especially *m* of the sodium channel
   #. Markov submodels may also be stiff systems so need the *markov_be* integration method.

   In this particular case, the sodium channel, *I_Na* on line 170, is definitely a culprit. After inspection,
   we see *diff_* defined as well as redundant alpha/beta/tau/_inf. This is what I finally changed it to::

    #I_Na
    I_Na = (I_Na_junc+I_Na_sl); .units(uA/uF);
    I_Na_junc = (Fjunc*GNa*(m*m*m)*h*j*(V_m - ena_junc)); .units(uA/uF);
    I_Na_sl = (Fsl*GNa*(m*m*m)*h*j*(V_m - ena_sl)); .units(uA/uF);
    ah = ((V_m>=-40.) ? 0. : (0.057*exp((-(V_m+80.)/6.8)))); .units(unitless);
    tau_h = (1./(ah+bh)); .units(ms);
    bh = ((V_m>=-40.) ? (0.77/(0.13*(1.+exp((-(V_m+10.66)/11.1))))) : ((2.7*exp((0.079*V_m)))+(3.1e5*exp((0.3485*V_m))))); .units(unitless);
    h_inf = (1./((1.+exp(((V_m+71.55)/7.43)))*(1.+exp(((V_m+71.55)/7.43))))); .units(unitless);
    tau_m = ((0.1292*exp(-(((V_m+45.79)/15.54)*((V_m+45.79)/15.54))))+(0.06487*exp(-(((V_m - 4.823)/51.12)*((V_m - 4.823)/51.12))))); .units(ms);
    m_inf = (1./((1.+exp((-(56.86+V_m)/9.03)))*(1.+exp((-(56.86+V_m)/9.03))))); .units(unitless);
    bj = ((V_m>=-40.) ? ((0.6*exp((0.057*V_m)))/(1.+exp((-0.1*(V_m+32.))))) : ((0.02424*exp((-0.01052*V_m)))/(1.+exp((-0.1378*(V_m+40.14)))))); .units(unitless);
    aj = ((V_m>=-40.) ? 0. : ((((-2.5428e4*exp((0.2444*V_m))) - (6.948e-6*exp((-0.04391*V_m))))*(V_m+37.78))/(1.+exp((0.311*(V_m+79.23)))))); .units(unitless);
    tau_j = (1./(aj+bj)); .units(ms);
    j_inf = (1./((1.+exp(((V_m+71.55)/7.43)))*(1.+exp(((V_m+71.55)/7.43))))); .units(unitless);

   We try to run it again and we still have an issue. As mentioned above, Markov chains and calcium handling can be
   numercially stiff. We will try more expensive integration methods at the cost of some speed. I added the following code
   to *grandi_pasqualini_bers_2010.model* ::

    group {
        Ca_i;
        Ca_j;
        Ca_sl;
        Ca_sr;
        f_Ca_Bj;
        f_Ca_Bsl;
    }.method(cvode);
    group {
        Ry_Ri;
        Ry_Ro;
        Ry_Rr;
    }.method(markov_be);

   This time, we can compile and run it. However, we are not done. Let's try to improve performance by
   using a lookup table for the voltage functions. We change line 2 of the model file to be ::

     V_m; .external(Vm); .nodal();.lookup(-100,100,0.05);

   We generate the C file, make the linkable library and when we try to run it::

    linux-nvs8%bench.debug.petsc.pt --load ./grandi_pasqualini_bers_2010.so --stim-start=100 --dt=0.005 -Oa

    L2 : LUT WARNING: grandi_pasqualini_bers_2010 V_m=-5 produces -nan in entry number 1!

    L2 : LUT WARNING: grandi_pasqualini_bers_2010 V_m=-5 produces -nan in entry number 2!

    Outputting the following quantities at each time:
          Time              Vm            Iion


    [CVODE ERROR]  CVode
      At t = 283.5 and h = 1.90735e-08, the corrector convergence test failed repeatedly or with |h| = hmin.

    bench.debug.petsc.pt: /home/vigmond/grandi_pasqualini_bers_2010.c:868: compute_grandi_pasqualini_bers_2010: Assertion `CVODE_flag == 0' failed.

   Hmmm. Maybe the NaN in the lookup table triggers the error. Sure enough, we see that entry for the d-gate time constant
   of I_Ca, *tau_d*, has  a singularity at -5 mV and that is where the simulation failed. We need to use L'Hopital's rule
   for that voltage::

    tau_d = (V_m==-5.)?(-d_inf/6./0.035):((1.*d_inf*(1. - exp((-(V_m+5.)/6.))))/(0.035*(V_m+5.))); .units(ms);
    d_inf = (1./(1.+exp((-(V_m+5.)/6.)))); .units(unitless);

   This :download:`model file </downloads/grandi_pasqualini_bers_2010_final.model>` now works!!!! For further practice, determine which subset of Ca variables can be removed from the group and/or
   if another integration method can be used.

"""


EXAMPLE_DESCRIPTIVE_NAME = 'Converting CellML'
EXAMPLE_AUTHOR = 'Edward Vigmond <edward.vigmond@u-bordeaux.fr>'
GUIinclude = False

from carputils import tools

def parser():
    """ Setup command line parser.
    """
    parser = tools.standard_parser(False)
    return parser

