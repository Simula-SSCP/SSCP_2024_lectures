"""
Implements widgets that are used in the E6 notebook. Each widget is 
implemented as a class that can be imported. To use a widget, create
an object of the class in question and call its display method.

Example:
========
from L6_widgets import VentricularAPWidget
VentricularAPWidget().display()
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import exp, log, sqrt, pi
from ipywidgets import interact, FloatSlider, Dropdown

class VentricularAPWidget():
    """A widget to solve the Grandi-Bers ventricular action potential model"""
    #----------------------------------------------------------------------------
    #The widget
     
    def __init__(self):
        interact(self.solve_and_plot,
                          epi_endo = Dropdown(options={'Epi': 1, 'Endo': 0},value=1,description='Cell type:'),
                          GNa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gNa scale factor', continuous_update=False),
                          GtoSlow_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gto,slow scale factor', continuous_update=False),
                          GtoFast_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gto,fast scale factor', continuous_update=False),
                          Gkr_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKr scale factor', continuous_update=False),
                          Gks_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKs scale factor', continuous_update=False),
                          Gkp_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKp scale factor', continuous_update=False),
                          Gk1_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gK1 scale factor', continuous_update=False),
                          GClCa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gClCa scale factor', continuous_update=False),
                          pCa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gCa scale factor', continuous_update=False),
                          VNCX_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='NCX Vmax scale factor', continuous_update=False),
                          VNaK_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='NKa Vmax scale factor', continuous_update=False),
                          GNaB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gNaB scale factor', continuous_update=False),
                          GCaB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gCaB scale factor', continuous_update=False),
                          GClB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gClB scale factor', continuous_update=False))
 
    #----------------------------------------------------------------------------
    #The run function
     
    def solve_and_plot(self,epi_endo, GNa_coeff, GtoSlow_coeff, GtoFast_coeff, Gkr_coeff, Gks_coeff, Gkp_coeff, 
                            Gk1_coeff, GClCa_coeff, pCa_coeff, VNCX_coeff, VNaK_coeff, GNaB_coeff, GCaB_coeff, GClB_coeff):
         
        Params_to_change = [epi_endo, GNa_coeff, GtoSlow_coeff, GtoFast_coeff, Gkr_coeff, Gks_coeff, Gkp_coeff, 
                            Gk1_coeff, GClCa_coeff, pCa_coeff, VNCX_coeff, VNaK_coeff, GNaB_coeff, GCaB_coeff, GClB_coeff] 
        
        
        Pd = set_Pd()
        y0 = Initialize(np.load('Widget_init.npy'))
        t = np.linspace(0,1000,1001)
        Y = odeint(grandi_bers_rhs, y0, t, (Pd,))
        plt.figure(1)
        plt.plot(t,Y[:, name2index("Vmo")]);
        plt.figure(2)
        plt.plot(t,Y[:, name2index("Caio")]*1000);
        Pd = set_Pd(Params_to_change)
        y0 = Initialize(np.load('Widget_init.npy'))
        t = np.linspace(0,1000,1001)
        Y = odeint(grandi_bers_rhs, y0, t, (Pd,))
        plt.figure(1)
        plt.plot(t,Y[:, name2index("Vmo")]);
        plt.legend((r'Default',r'$new$'))
        plt.ylabel('V(mV)')
        plt.figure(2)
        plt.plot(t,Y[:, name2index("Caio")]*1000);
        plt.legend((r'Default',r'$new$'))
        plt.ylabel('Ca_i(uM)')
        plt.xlabel('time (ms)')
        plt.show();
 
class VentricularAPWidget2():
    """A widget to solve the Grandi-Bers ventricular action potential model 
        and allow it to be reduced to the atrial model"""
    #----------------------------------------------------------------------------
    #The widget
    
    def __init__(self):
        interact(self.solve_and_plot,
                          epi_endo = Dropdown(options={'Epi': 1, 'Endo': 0},value=1,description='Cell type:'),
                          GNa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gNa scale factor', continuous_update=False),
                          GtoSlow_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gto,slow scale factor', continuous_update=False),
                          GtoFast_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gto,fast scale factor', continuous_update=False),
                          Gkr_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKr scale factor', continuous_update=False),
                          Gks_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKs scale factor', continuous_update=False),
                          Gkp_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKp scale factor', continuous_update=False),
                          Gk1_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gK1 scale factor', continuous_update=False),
                          GClCa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gClCa scale factor', continuous_update=False),
                          pCa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gCa scale factor', continuous_update=False),
                          VNCX_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='NCX Vmax scale factor', continuous_update=False),
                          VNaK_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='NKa Vmax scale factor', continuous_update=False),
                          GNaB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gNaB scale factor', continuous_update=False),
                          GCaB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gCaB scale factor', continuous_update=False),
                          GClB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gClB scale factor', continuous_update=False))


    #----------------------------------------------------------------------------
    #The run function
    
    def solve_and_plot(self,epi_endo, GNa_coeff, GtoSlow_coeff, GtoFast_coeff, Gkr_coeff, Gks_coeff, Gkp_coeff, 
                            Gk1_coeff, GClCa_coeff, pCa_coeff, VNCX_coeff, VNaK_coeff, GNaB_coeff, GCaB_coeff, GClB_coeff):
        
        Params_to_change = [epi_endo, GNa_coeff, GtoSlow_coeff, GtoFast_coeff, Gkr_coeff, Gks_coeff, Gkp_coeff, 
                            Gk1_coeff, GClCa_coeff, pCa_coeff, VNCX_coeff, VNaK_coeff, GNaB_coeff, GCaB_coeff, GClB_coeff] 
        
        Pd = set_Pd()
        y0 = Initialize(np.load('Widget_init.npy'))
        t = np.linspace(0,1000,1001)
        Y = odeint(grandi_bers_rhs, y0, t, (Pd,))
        plt.figure(1)
        plt.plot(t,Y[:, name2index("Vmo")])
        plt.figure(2)
        plt.plot(t,Y[:, name2index("Caio")]*1000)
        
        Pd_atrial = set_Pd_atrial()
        y0 = Initialize_atrial(np.load('Widget_init_atrial.npy'))
        t = np.linspace(0,1000,1001)
        Y = odeint(grandi_bers_rhs_atrial, y0, t, (Pd_atrial,))
        plt.figure(1)
        plt.plot(t,Y[:, name2index_atrial("Vmo")])
        plt.figure(2)
        plt.plot(t,Y[:, name2index_atrial("Caio")]*1000)
        
        Pd = set_Pd(Params_to_change)
        y0 = Initialize(np.load('Widget_init.npy'))
        t = np.linspace(0,1000,1001)
        Y = odeint(grandi_bers_rhs, y0, t, (Pd,))
        plt.figure(1)
        plt.plot(t,Y[:, name2index("Vmo")])
        plt.legend((r'Ventricular',r'Atrial',r'$new$ Ventricular'))
        plt.ylabel('V(mV)')
        plt.figure(2)
        plt.plot(t,Y[:, name2index("Caio")]*1000)
        plt.legend((r'Ventricular',r'Atrial',r'$new$ Ventricular'))
        plt.ylabel('Ca_i(uM)')
        plt.xlabel('time (ms)')
        plt.show()


class AtrialAPWidget():
    """A widget to solve the Grandi-Bers atrial action potential model and allow it to be pushed toward the 
    ventricular model"""
    #----------------------------------------------------------------------------
    #The widget
    
    def __init__(self):
        interact(self.solve_and_plot,        
                          GNa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gNa scale factor', continuous_update=False),
                          GtoFast_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gto,fast scale factor', continuous_update=False),
                          Gkr_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKr scale factor', continuous_update=False),
                          Gkur_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKur scale factor', continuous_update=False),
                          Gks_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKs scale factor', continuous_update=False),
                          Gkp_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKp scale factor', continuous_update=False),
                          Gk1_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gK1 scale factor', continuous_update=False),
                          GClCa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gClCa scale factor', continuous_update=False),
                          pCa_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gCa scale factor', continuous_update=False),
                          VNCX_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='NCX Vmax scale factor', continuous_update=False),
                          VNaK_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='NKa Vmax scale factor', continuous_update=False),
                          GNaB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gNaB scale factor', continuous_update=False),
                          GCaB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gCaB scale factor', continuous_update=False),
                          GClB_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gClB scale factor', continuous_update=False),
                          GkAch_coeff = FloatSlider(value=1, min=0, max=10, step=0.1, description='gKAch scale factor', continuous_update=False),
                          Ach = FloatSlider(value=0, min=0, max=0.1, step=0.001, description='Ach scale factor', continuous_update=False))


    #----------------------------------------------------------------------------
    #The run function
    
    def solve_and_plot(self,GNa_coeff, GtoFast_coeff, Gkur_coeff, Gkr_coeff, Gks_coeff, Gkp_coeff, 
                       Gk1_coeff, GClCa_coeff, pCa_coeff, VNCX_coeff, VNaK_coeff, GNaB_coeff, GCaB_coeff, GClB_coeff, GkAch_coeff, Ach):
        
        Params_to_change = [GNa_coeff, GtoFast_coeff, Gkr_coeff, Gkur_coeff, Gks_coeff, Gkp_coeff, 
                            Gk1_coeff, GClCa_coeff, pCa_coeff, VNCX_coeff, VNaK_coeff, GNaB_coeff, GCaB_coeff, GClB_coeff, GkAch_coeff, Ach] 
        
        Pd_atrial = set_Pd_atrial()
        y0 = Initialize_atrial(np.load('Widget_init_atrial.npy'))
        t = np.linspace(0,1000,1001)
        Y = odeint(grandi_bers_rhs_atrial, y0, t, (Pd_atrial,))
        plt.figure(1)
        plt.plot(t,Y[:, name2index_atrial("Vmo")])
        plt.figure(2)
        plt.plot(t,Y[:, name2index_atrial("Caio")]*1000)
        
        Pd = set_Pd()
        y0 = Initialize(np.load('Widget_init.npy'))
        t = np.linspace(0,1000,1001)
        Y = odeint(grandi_bers_rhs, y0, t, (Pd,))
        plt.figure(1)
        plt.plot(t,Y[:,name2index("Vmo")])
        plt.figure(2)
        plt.plot(t,Y[:,name2index("Caio")]*1000)
        
        Pd_atrial = set_Pd_atrial(Params_to_change)
        y0 = Initialize_atrial(np.load('Widget_init_atrial.npy'))
        t = np.linspace(0,1000,1001)
        Y = odeint(grandi_bers_rhs_atrial, y0, t, (Pd_atrial,))
        plt.figure(1)
        plt.plot(t,Y[:,name2index_atrial("Vmo")])
        plt.legend((r'Atrial',r'Ventricular',r'$new$ Atrial'))
        plt.figure(2)
        plt.plot(t,Y[:,name2index_atrial("Caio")]*1000)
        plt.legend((r'Atrial',r'Ventricular',r'$new$ Atrial'))
        plt.show()
#----------------------------------------------------------------------------
# Global functions
# Ventricular first
def grandi_bers_rhs(y, t, Pd):
    m,     h,     j,     d,     f,     fcaBj,     fcaBsl,    xtos,     ytos,     xtof,     ytof,     xkr,     xks,     RyRr,    RyRo,    RyRi,    NaBj,    NaBsl,    TnCL,     TnCHc,    TnCHm,    CaM,     Myoc,     Myom,     SRB,     SLLj,     SLLsl,     SLHj,     SLHsl,     Csqnb,     Ca_sr,    Naj,     Nasl,     Nai,     Ki,     Caj,     Casl,    Cai,     Vm  = y

    # Constants
    R = Pd['R']
    Frdy = Pd['Frdy']
    Temp = Pd['Temp']
    FoRT = Frdy/R/Temp
    Qpow = (Temp-310)/10
    Cmem = Pd['Cmem']

    # Cell geometry
    Vcell = pi*Pd['cellRadius']**2*Pd['cellLength']*1e-15 
    Vmyo = Pd['Vmyo_ratio']*Vcell
    Vsr = Pd['Vsr_ratio']*Vcell
    Vsl = Pd['Vsl_ratio']*Vcell
    Vjunc = Pd['Vjunc_ratio']*Vcell

    # Fractional currents in compartments
    Fjunc = Pd['Fjunc']
    Fsl = 1-Fjunc
    Fjunc_CaL = Pd['Fjunc_CaL'] 
    Fsl_CaL = 1-Fjunc_CaL

    # Fixed ion concentrations     
    Cli = Pd['Cli']
    Clo = Pd['Clo']
    Ko = Pd['Ko']
    Nao = Pd['Nao']
    Cao = Pd['Cao']
    Mgi = Pd['Mgi']

    # Buffering parameters
    # koff: [1/s] = 1e-3*[1/ms]  kon: [1/uM/s] = [1/mM/ms]
    Bmax_Naj = Pd['Bmax_Naj']
    Bmax_Nasl = Pd['Bmax_Nasl']
    koff_na = Pd['koff_na']
    kon_na = Pd['kon_na']
    Bmax_TnClow = Pd['Bmax_TnClow']
    koff_tncl = Pd['koff_tncl']
    kon_tncl = Pd['kon_tncl'] 
    Bmax_TnChigh = Pd['Bmax_TnChigh']
    koff_tnchca = Pd['koff_tnchca']
    kon_tnchca = Pd['kon_tnchca'] 
    koff_tnchmg = Pd['koff_tnchmg']
    kon_tnchmg = Pd['kon_tnchmg'] 
    Bmax_CaM = Pd['Bmax_CaM'] 
    koff_cam = Pd['koff_cam'] 
    kon_cam = Pd['kon_cam'] 
    Bmax_myosin = Pd['Bmax_myosin']
    koff_myoca = Pd['koff_myoca']
    kon_myoca = Pd['kon_myoca']
    koff_myomg = Pd['koff_myomg']
    kon_myomg = Pd['kon_myomg']
    Bmax_SR = Pd['Bmax_SR']
    koff_sr = Pd['koff_sr']
    kon_sr = Pd['kon_sr']
    Bmax_SLlowsl = Pd['Bmax_SLlowsl']*Vmyo/Vsl        # [mM]    # SL buffering
    Bmax_SLlowj = Pd['Bmax_SLlowj']*Vmyo/Vjunc    # [mM]   
    koff_sll = Pd['koff_sll']    # [1/ms]
    kon_sll = Pd['kon_sll']          # [1/mM/ms]
    Bmax_SLhighsl = Pd['Bmax_SLhighsl']*Vmyo/Vsl       # [mM] 
    Bmax_SLhighj = Pd['Bmax_SLhighj']*Vmyo/Vjunc  # [mM] 
    koff_slh = Pd['koff_slh']     # [1/ms]
    kon_slh = Pd['kon_slh']          # [1/mM/ms]
    Bmax_Csqn = Pd['Bmax_Csqn']*Vmyo/Vsr  # [mM] # Bmax_Csqn = 2.6      # Csqn buffering
    koff_csqn = Pd['koff_csqn']
    kon_csqn = Pd['kon_csqn']

    #########################33

    # Nernst Potentials
    ena_junc = (1/FoRT)*log(Nao/Naj)     # [mV]
    ena_sl = (1/FoRT)*log(Nao/Nasl)       # [mV]
    ek = (1/FoRT)*log(Ko/Ki)	        # [mV]
    eca_junc = (1/FoRT/2)*log(Cao/Caj)   # [mV]
    eca_sl = (1/FoRT/2)*log(Cao/Casl)     # [mV]
    ecl = (1/FoRT)*log(Cli/Clo)            # [mV]

    #CURRENTS
    #INa ten Tusscher formulation
    mss = 1 / ((1 + exp( -(56.86 + Vm) / 9.03 ))**2)
    taum = 0.1292 * exp(-((Vm+45.79)/15.54)**2) + 0.06487 * exp(-((Vm-4.823)/51.12)**2)                 
    ah = 0.0 if (Vm >= -40) else (0.057 * exp( -(Vm + 80) / 6.8 )) 
    bh =  (0.77 / (0.13*(1 + exp( -(Vm + 10.66) / 11.1 )))) if (Vm >= -40) else ((2.7 * exp( 0.079 * Vm) + 3.1*10**5 * exp(0.3485 * Vm))) 
    tauh = 1 / (ah + bh) 
    hss = 1 / ((1 + exp( (Vm + 71.55)/7.43 ))**2)
    aj = (0) if (Vm >= -40) else (((-2.5428 * 10**4*exp(0.2444*Vm) - 6.948*10**-6 * exp(-0.04391*Vm)) * (Vm + 37.78)) /(1 + exp( 0.311 * (Vm + 79.23) )))
    bj =  ((0.6 * exp( 0.057 * Vm)) / (1 + exp( -0.1 * (Vm + 32) ))) if (Vm >= -40) else ((0.02424 * exp( -0.01052 * Vm )) / (1 + exp( -0.1378 * (Vm + 40.14) ))) 
    tauj = 1 / (aj + bj)
    jss = 1 / ((1 + exp( (Vm + 71.55)/7.43 ))**2)         
    d_m = (mss - m) / taum
    d_h = (hss - h) / tauh
    d_j = (jss - j) / tauj
    I_Na_junc = Fjunc*Pd['GNa']*m**3*h*j*(Vm-ena_junc)
    I_Na_sl = Fsl*Pd['GNa']*m**3*h*j*(Vm-ena_sl)
    I_Na = I_Na_junc+I_Na_sl

    # I_nak: Na/K Pump Current
    sigma = (exp(Nao/67.3)-1)/7
    fnak = 1/(1+0.1245*exp(-0.1*Vm*FoRT)+0.0365*sigma*exp(-Vm*FoRT))
    I_nak_junc = 1*Fjunc*Pd['IbarNaK']*fnak*Ko/(1+(Pd['KmNaip']/Naj)**4)/(Ko+Pd['KmKo'])
    I_nak_sl = 1*Fsl*Pd['IbarNaK']*fnak*Ko/(1+(Pd['KmNaip']/Nasl)**4)/(Ko+Pd['KmKo'])
    I_nak = I_nak_junc+I_nak_sl

    ## I_kr: Rapidly Activating K Current
    gkr = Pd['Gkr']*sqrt(Ko/5.4)
    xrss = 1/(1+exp(-(Vm+10)/5))
    tauxr = 550/(1+exp((-22-Vm)/9))*6/(1+exp((Vm-(-11))/9))+230/(1+exp((Vm-(-40))/20))
    d_xkr = (xrss-xkr)/tauxr
    rkr = 1/(1+exp((Vm+74)/24))
    I_kr = gkr*xkr*rkr*(Vm-ek)

    ## I_ks: Slowly Activating K Current
    eks = (1/FoRT)*log((Ko+Pd['pNaK']*Nao)/(Ki+Pd['pNaK']*Nai))
    gks_junc=1*0.0035
    gks_sl=1*0.0035 #FRA
    xsss = 1 / (1+exp(-(Vm + 3.8)/14.25)) # fitting Fra
    tauxs=990.1/(1+exp(-(Vm+2.436)/14.12))
    d_xks = (xsss-xks)/tauxs
    I_ks_junc = Fjunc*Pd['Gks']*xks**2*(Vm-eks)
    I_ks_sl = Fsl*Pd['Gks']*xks**2*(Vm-eks)      
    I_ks = I_ks_junc+I_ks_sl
     
    # I_kp: Plateau K current
    kp_kp = 1/(1+exp(7.488-Vm/5.98))
    I_kp_junc = Fjunc*Pd['Gkp']*kp_kp*(Vm-ek)
    I_kp_sl = Fsl*Pd['Gkp']*kp_kp*(Vm-ek)
    I_kp = I_kp_junc+I_kp_sl

    ## I_to: Transient Outward K Current (slow and fast components)
    I_tos = Pd['GtoSlow']*xtos*ytos*(Vm-ek)   
    I_tof = Pd['GtoFast']*xtof*ytof*(Vm-ek)
    xtoss = 1/(1+exp(-(Vm-19.0)/13))
    ytoss = 1/(1+exp((Vm+19.5)/5))
    tauxtos = 9/(1+exp((Vm+3.0)/15))+0.5
    tauytos = 800/(1+exp((Vm+60.0)/10))+30
    d_xtos = (xtoss-xtos)/tauxtos
    d_ytos = (ytoss-ytos)/tauytos
    tauxtof = 11*exp(-((Vm+45)/60)**2)+1.0 
    tauytof = 85*exp((-(Vm+40)**2/220))+7
    d_xtof = (xtoss-xtof)/tauxtof
    d_ytof = (ytoss-ytof)/tauytof
    I_to = I_tos + I_tof

    ## I_ki: Time-Independent K Current
    aki = 1.02/(1+exp(0.2385*(Vm-ek-59.215)))
    bki =(0.49124*exp(0.08032*(Vm+5.476-ek)) + exp(0.06175*(Vm-ek-594.31))) /(1 + exp(-0.5143*(Vm-ek+4.753)))
    kiss = aki/(aki+bki)
    I_ki = Pd['Gki']*sqrt(Ko/5.4)*kiss*(Vm-ek)

    # I_ClCa: Ca-activated Cl Current, I_Clbk: background Cl Current
    I_ClCa_junc = Fjunc*Pd['GClCa']/(1+Pd['KdClCa']/Caj)*(Vm-ecl)
    I_ClCa_sl = Fsl*Pd['GClCa']/(1+Pd['KdClCa']/Casl)*(Vm-ecl)
    I_ClCa = I_ClCa_junc+I_ClCa_sl  
    
    ## I_Ca: L-type Calcium Current  
    dss = 1/(1+exp(-(Vm+5)/6.0))
    fss = 1/(1+exp((Vm+35)/9))+0.6/(1+exp((50-Vm)/20))
    taud = dss*(1-exp(-(Vm+5)/6.0))/(0.035*(Vm+5))
    tauf = 1/(0.0197*exp( -(0.0337*(Vm+14.5))**2 )+0.02)
    d_d = (dss-d)/taud
    d_f = (fss-f)/tauf
    d_fcaBj = 1.7*Caj*(1-fcaBj)-11.9e-3*fcaBj # fCa_junc   koff!!!!!!!!
    d_fcaBsl = 1.7*Casl*(1-fcaBsl)-11.9e-3*fcaBsl # fCa_sl
    fcaCaMSL= 0.1/(1+(0.01/Casl))
    fcaCaj= 0.1/(1+(0.01/Caj))
    fcaCaMSL=0
    fcaCaj= 0
    ibarca_j = Pd['pCa']*4*(Vm*Frdy*FoRT) * (0.341*Caj*exp(2*Vm*FoRT)-0.341*Cao) /(exp(2*Vm*FoRT)-1)
    ibarca_sl = Pd['pCa']*4*(Vm*Frdy*FoRT) * (0.341*Casl*exp(2*Vm*FoRT)-0.341*Cao) /(exp(2*Vm*FoRT)-1)
    ibark = Pd['pK']*(Vm*Frdy*FoRT)*(0.75*Ki*exp(Vm*FoRT)-0.75*Ko) /(exp(Vm*FoRT)-1)
    ibarna_j = Pd['pNa']*(Vm*Frdy*FoRT) *(0.75*Naj*exp(Vm*FoRT)-0.75*Nao)  /(exp(Vm*FoRT)-1)
    ibarna_sl = Pd['pNa']*(Vm*Frdy*FoRT) *(0.75*Nasl*exp(Vm*FoRT)-0.75*Nao)  /(exp(Vm*FoRT)-1)
    I_Ca_junc = (Fjunc_CaL*ibarca_j*d*f*((1-fcaBj)+fcaCaj)*Pd['Q10CaL']**Qpow)*0.45*1
    I_Ca_sl = (Fsl_CaL*ibarca_sl*d*f*((1-fcaBsl)+fcaCaMSL)*Pd['Q10CaL']**Qpow)*0.45*1
    I_Ca = I_Ca_junc+I_Ca_sl
    I_CaK = (ibark*d*f*(Fjunc_CaL*(fcaCaj+(1-fcaBj))+Fsl_CaL*(fcaCaMSL+(1-fcaBsl)))*Pd['Q10CaL']**Qpow)*0.45*1
    I_CaNa_junc = (Fjunc_CaL*ibarna_j*d*f*((1-fcaBj)+fcaCaj)*Pd['Q10CaL']**Qpow)*0.45*1
    I_CaNa_sl = (Fsl_CaL*ibarna_sl*d*f*((1-fcaBsl)+fcaCaMSL)*Pd['Q10CaL']**Qpow)*.45*1
    I_CaNa = I_CaNa_junc+I_CaNa_sl
    I_Catot = I_Ca+I_CaK+I_CaNa

    # I_ncx: Na/Ca Exchanger flux
    Ka_junc = 1/(1+(Pd['Kdact']/Caj)**2)
    Ka_sl = 1/(1+(Pd['Kdact']/Casl)**2)
    s1_junc = exp(Pd['nu']*Vm*FoRT)*Naj**3*Cao
    s1_sl = exp(Pd['nu']*Vm*FoRT)*Nasl**3*Cao
    s2_junc = exp((Pd['nu']-1)*Vm*FoRT)*Nao**3*Caj
    s3_junc = Pd['KmCai']*Nao**3*(1+(Naj/Pd['KmNai'])**3) + Pd['KmNao']**3*Caj*(1+Caj/Pd['KmCai'])+Pd['KmCao']*Naj**3+Naj**3*Cao+Nao**3*Caj
    s2_sl = exp((Pd['nu']-1)*Vm*FoRT)*Nao**3*Casl
    s3_sl = Pd['KmCai']*Nao**3*(1+(Nasl/Pd['KmNai'])**3) + Pd['KmNao']**3*Casl*(1+Casl/Pd['KmCai'])+Pd['KmCao']*Nasl**3+Nasl**3*Cao+Nao**3*Casl
    I_ncx_junc = Fjunc*Pd['IbarNCX']*Pd['Q10NCX']**Qpow*Ka_junc*(s1_junc-s2_junc)/s3_junc/(1+Pd['ksat']*exp((Pd['nu']-1)*Vm*FoRT))
    I_ncx_sl = Fsl*Pd['IbarNCX']*Pd['Q10NCX']**Qpow*Ka_sl*(s1_sl-s2_sl)/s3_sl/(1+Pd['ksat']*exp((Pd['nu']-1)*Vm*FoRT))
    I_ncx = I_ncx_junc+I_ncx_sl

    # I_pca: Sarcolemmal Ca Pump Current
    I_pca_junc = Fjunc*Pd['Q10SLCaP']**Qpow*Pd['IbarSLCaP']*Caj**1.6/(Pd['KmPCa']**1.6+Caj**1.6)
    I_pca_sl = Fsl*Pd['Q10SLCaP']**Qpow*Pd['IbarSLCaP']*Casl**1.6/(Pd['KmPCa']**1.6+Casl**1.6)
    I_pca = I_pca_junc+I_pca_sl

    ## SR fluxes: Calcium Release, SR Ca pump, SR Ca leak
    MaxSR = 15 
    MinSR = 1
    kCaSR = MaxSR - (MaxSR-MinSR)/(1+(Pd['ec50SR']/Ca_sr)**2.5)
    koSRCa = Pd['koCa']/kCaSR
    kiSRCa = Pd['kiCa']*kCaSR
    RI = 1-RyRr-RyRo-RyRi
    d_RyRr = (Pd['kim']*RI-kiSRCa*Caj*RyRr)-(koSRCa*Caj**2*RyRr-Pd['kom']*RyRo)   # R
    d_RyRo = (koSRCa*Caj**2*RyRr-Pd['kom']*RyRo)-(kiSRCa*Caj*RyRo-Pd['kim']*RyRi)# O
    d_RyRi = (kiSRCa*Caj*RyRo-Pd['kim']*RyRi)-(Pd['kom']*RyRi-koSRCa*Caj**2*RI)   # I
    J_SRCarel = Pd['ks']*RyRo*(Ca_sr-Caj)          # [mM/ms]
    J_serca = 1*Pd['Q10SRCaP']**Qpow*Pd['Vmax_SRCaP']*((Cai/Pd['Kmf'])**Pd['hillSRCaP']-(Ca_sr/Pd['Kmr'])**Pd['hillSRCaP'])/(1+(Cai/Pd['Kmf'])**Pd['hillSRCaP']+(Ca_sr/Pd['Kmr'])**Pd['hillSRCaP'])
    J_SRleak = 5.348e-6*(Ca_sr-Caj)           #   [mM/ms]

    # BACKROUND CURRENTS
    # I_nabk: Na Background Current
    I_nabk_junc = Fjunc*Pd['GNaB']*(Vm-ena_junc)
    I_nabk_sl = Fsl*Pd['GNaB']*(Vm-ena_sl)
    I_nabk = I_nabk_junc+I_nabk_sl
    
    # I_cabk: Ca Background Current
    I_cabk_junc = Fjunc*Pd['GCaB']*(Vm-eca_junc)
    I_cabk_sl = Fsl*Pd['GCaB']*(Vm-eca_sl)
    I_cabk = I_cabk_junc+I_cabk_sl
    
    # I_Clbk: Chloride Background Current
    I_Clbk = Pd['GClB']*(Vm-ecl) 

    # BUFFERS
    # Sodium and Calcium Buffering
    d_NaBj = kon_na*Naj*(Bmax_Naj-NaBj)-koff_na*NaBj        # NaBj      [mM/ms]
    d_NaBsl = kon_na*Nasl*(Bmax_Nasl-NaBsl)-koff_na*NaBsl       # NaBsl     [mM/ms]

    # Cytosolic Ca Buffers
    d_TnCL = kon_tncl*Cai*(Bmax_TnClow-TnCL)-koff_tncl*TnCL            # TnCL      [mM/ms]
    d_TnCHc = kon_tnchca*Cai*(Bmax_TnChigh-TnCHc-TnCHm)-koff_tnchca*TnCHc # TnCHc     [mM/ms]
    d_TnCHm = kon_tnchmg*Mgi*(Bmax_TnChigh-TnCHc-TnCHm)-koff_tnchmg*TnCHm   # TnCHm     [mM/ms]
    d_CaM = kon_cam*Cai*(Bmax_CaM-CaM)-koff_cam*CaM                 # CaM       [mM/ms]
    d_Myoc = kon_myoca*Cai*(Bmax_myosin-Myoc-Myom)-koff_myoca*Myoc    # Myosin_ca [mM/ms]
    d_Myom = kon_myomg*Mgi*(Bmax_myosin-Myoc-Myom)-koff_myomg*Myom      # Myosin_mg [mM/ms]
    d_SRB = kon_sr*Cai*(Bmax_SR-SRB)-koff_sr*SRB                    # SRB       [mM/ms]
    J_CaB_cytosol = d_TnCL + d_TnCHc + d_TnCHm + d_CaM + d_Myoc + d_Myom + d_SRB

    # Junctional and SL Ca Buffers
    d_SLLj = kon_sll*Caj*(Bmax_SLlowj-SLLj)-koff_sll*SLLj       # SLLj      [mM/ms]
    d_SLLsl = kon_sll*Casl*(Bmax_SLlowsl-SLLsl)-koff_sll*SLLsl      # SLLsl     [mM/ms]
    d_SLHj = kon_slh*Caj*(Bmax_SLhighj-SLHj)-koff_slh*SLHj      # SLHj      [mM/ms]
    d_SLHsl = kon_slh*Casl*(Bmax_SLhighsl-SLHsl)-koff_slh*SLHsl     # SLHsl     [mM/ms]
    J_CaB_junction = d_SLLj+d_SLHj
    J_CaB_sl = d_SLLsl+d_SLHsl

    ## Ion concentrations
    # SR Ca Concentrations
    d_Csqnb = kon_csqn*Ca_sr*(Bmax_Csqn-Csqnb)-koff_csqn*Csqnb       # Csqn      [mM/ms]
    d_Ca_sr = J_serca-(J_SRleak*Vmyo/Vsr+J_SRCarel)-d_Csqnb         # Ca_sr     [mM/ms] #Ratio 3 leak current
    # d_Ca_sr=0

    # Sodium Concentrations
    I_Na_tot_junc = I_Na_junc+I_nabk_junc+3*I_ncx_junc+3*I_nak_junc+I_CaNa_junc   # [uA/uF]
    I_Na_tot_sl = I_Na_sl+I_nabk_sl+3*I_ncx_sl+3*I_nak_sl+I_CaNa_sl   # [uA/uF]
    I_Na_tot_sl2 = 3*I_ncx_sl+3*I_nak_sl+I_CaNa_sl   # [uA/uF]
    I_Na_tot_junc2 = 3*I_ncx_junc+3*I_nak_junc+I_CaNa_junc   # [uA/uF]
    d_Naj = -I_Na_tot_junc*Cmem/(Vjunc*Frdy)+Pd['J_na_juncsl']/Vjunc*(Nasl-Naj)-d_NaBj
    d_Nasl = -I_Na_tot_sl*Cmem/(Vsl*Frdy)+Pd['J_na_juncsl']/Vsl*(Naj-Nasl)+Pd['J_na_slmyo']/Vsl*(Nai-Nasl)-d_NaBsl

    #FluxNaSL=d_Nasl
    d_Nai = Pd['J_na_slmyo']/Vmyo*(Nasl-Nai)             # [mM/msec] 
    
    # Potassium Concentration
    I_K_tot = I_to+I_kr+I_ks+I_ki-2*I_nak+I_CaK+I_kp     # [uA/uF]
    d_Ki =0 # -I_K_tot*Cmem/(Vmyo*Frdy)

    # Calcium Concentrations
    I_Ca_tot_junc = I_Ca_junc+I_cabk_junc+I_pca_junc-2*I_ncx_junc                   # [uA/uF]
    I_Ca_tot_sl = I_Ca_sl+I_cabk_sl+I_pca_sl-2*I_ncx_sl            # [uA/uF]
    d_Caj = -I_Ca_tot_junc*Cmem/(Vjunc*2*Frdy)+Pd['J_ca_juncsl']/Vjunc*(Casl-Caj)   -J_CaB_junction+(J_SRCarel)*Vsr/Vjunc+J_SRleak*Vmyo/Vjunc  # Ca_j
    d_Casl = -I_Ca_tot_sl*Cmem/(Vsl*2*Frdy)+Pd['J_ca_juncsl']/Vsl*(Caj-Casl)  + Pd['J_ca_slmyo']/Vsl*(Cai-Casl)-J_CaB_sl   # Ca_sl
    d_Cai = -J_serca*Vsr/Vmyo-J_CaB_cytosol +Pd['J_ca_slmyo']/Vmyo*(Casl-Cai)

    ## Summing the current components
    I_Na_tot = I_Na_tot_junc + I_Na_tot_sl          # [uA/uF]
    I_Cl_tot = I_ClCa+I_Clbk                        # [uA/uF]
    I_Ca_tot = I_Ca_tot_junc+I_Ca_tot_sl
    I_tot = I_Na_tot+I_Cl_tot+I_Ca_tot+I_K_tot
    I_app = Pd['I_app'] if (t<5) else 0.0
    d_Vm = -(I_tot-I_app)

    ydot = [d_m,d_h, d_j, d_d, d_f,d_fcaBj, d_fcaBsl, d_xtos, d_ytos,d_xtof, d_ytof, d_xkr, d_xks, d_RyRr, d_RyRo, d_RyRi, d_NaBj, d_NaBsl, d_TnCL, d_TnCHc, d_TnCHm, d_CaM, d_Myoc, d_Myom,  d_SRB, d_SLLj, d_SLLsl, d_SLHj, d_SLHsl, d_Csqnb, d_Ca_sr, d_Naj, d_Nasl, d_Nai, d_Ki, d_Caj, d_Casl, d_Cai, d_Vm]

    ydot = list(map(lambda x,y:x*y, ydot, Pd['dynamic']))

    return ydot

#----------------------------------------------------------------------------
# Define the default parameter set as a dictionary, and accept changes from the sliders
def set_Pd(Params_to_change = None):
     
    if Params_to_change is None:
        epi_endo = 1
        GNa_coeff = 1
        GtoSlow_coeff = 1
        GtoFast_coeff = 1
        Gkr_coeff = 1
        Gks_coeff = 1
        Gkp_coeff = 1
        Gk1_coeff = 1
        GClCa_coeff = 1
        pCa_coeff = 1
        VNCX_coeff = 1
        VNaK_coeff = 1
        GNaB_coeff = 1
        GCaB_coeff = 1
        GClB_coeff = 1
    else:
        epi_endo = Params_to_change[0]
        GNa_coeff = Params_to_change[1]
        GtoSlow_coeff = Params_to_change[2]
        GtoFast_coeff = Params_to_change[3]
        Gkr_coeff = Params_to_change[4]
        Gks_coeff = Params_to_change[5]
        Gkp_coeff = Params_to_change[6]
        Gk1_coeff = Params_to_change[7]
        GClCa_coeff = Params_to_change[8]
        pCa_coeff = Params_to_change[9]
        VNCX_coeff = Params_to_change[10]
        VNaK_coeff = Params_to_change[11]
        GNaB_coeff = Params_to_change[12]
        GCaB_coeff = Params_to_change[13]
        GClB_coeff = Params_to_change[14]
     
    Pd = {}
    ## Model Parameters
    ## EPI or ENDO?
    Pd['epi']=1*epi_endo
    
    Pd['I_app'] = 6
    
    # Constants
    Pd['R'] = 8314       # [J/kmol*K]  
    Pd['Frdy'] = 96485   # [C/mol]  
    Pd['Temp'] = 310     # [K]
    Pd['Cmem'] = 1.3810e-10   # [F] membrane capacitance
    
    # Cell geometry
    Pd['cellLength'] = 100     # cell length [um]
    Pd['cellRadius'] = 10.25   # cell radius [um]
    Pd['Vmyo_ratio'] = 0.65
    Pd['Vsr_ratio'] = 0.035
    Pd['Vsl_ratio'] = 0.02
    Pd['Vjunc_ratio'] = 0.00539
    
    # Inter-compartmental fluxes
    Pd['J_ca_juncsl'] =1/1.2134e12 # [L/msec] = 8.2413e-13
    Pd['J_ca_slmyo'] = 1/2.68510e11 # [L/msec] = 3.2743e-12
    Pd['J_na_juncsl'] = 1/(1.6382e12/3*100) # [L/msec] = 6.1043e-13
    Pd['J_na_slmyo'] = 1/(1.8308e10/3*100)  # [L/msec] = 5.4621e-11
    
    # Fractional currents in compartments
    Pd['Fjunc'] = 0.11   
    Pd['Fjunc_CaL'] = 0.9 
    
    # Fixed ion concentrations     
    Pd['Cli'] = 15   # Intracellular Cl  [mM]
    Pd['Clo'] = 150  # Extracellular Cl  [mM]
    Pd['Ko']= 5.4   # Extracellular K   [mM]
    Pd['Nao'] = 140  # Extracellular Na  [mM]
    Pd['Cao'] = 1.8  # Extracellular Ca  [mM]1.8
    Pd['Mgi'] = 1.    # Intracellular Mg  [mM]
    
    # Na transport parameters
    Pd['GNa']=23*GNa_coeff
    Pd['GNaB'] = 0.597e-3*GNaB_coeff    # [mS/uF] 0.897e-3
    Pd['IbarNaK'] = 1.0*1.8*VNaK_coeff#1.90719;     # [uA/uF]
    Pd['KmNaip'] = 11        # [mM]11
    Pd['KmKo'] =1.5         # [mM]1.5
    Pd['Q10NaK'] = 1.63  
    Pd['Q10KmNai'] = 1.39
    
    ## K current parameters
    Pd['pNaK'] = 0.01833      
    Pd['Gkp'] = 2*0.001*Gkp_coeff 
    Pd['Gkr'] = 0.035*Gkr_coeff
    Pd['Gki'] = 0.35*Gk1_coeff
    Pd['Gks'] = 0.0035*Gks_coeff
    if Pd['epi']==1:
        Pd['GtoSlow'] = 1.0*0.13*0.12*GtoSlow_coeff #epi
        Pd['GtoFast'] = 1.0*0.13*0.88*GtoFast_coeff #epi0.88
    else:
        Pd['GtoSlow'] = 0.13*0.3*0.964*GtoSlow_coeff #endo
        Pd['GtoFast'] = 0.13*0.3*0.036*GtoFast_coeff #endo
    Pd['markov_iks'] = 0  
    
    # Cl current parameters
    Pd['GClCa'] =0.5*0.109625*GClCa_coeff   # [mS/uF]
    Pd['GClB'] = 1*9e-3*GClB_coeff        # [mS/uF]
    Pd['KdClCa'] = 100e-3    # [mM]
    
    # I_Ca parameters
    Pd['pNa'] = 0.50*1.5e-8       # [cm/sec]
    Pd['pCa'] = 0.50*5.4e-4*pCa_coeff      # [cm/sec]
    Pd['pK'] = 0.50*2.7e-7        # [cm/sec]
    Pd['Q10CaL'] = 1.8       
    
    ## Ca transport parameters
    Pd['IbarNCX'] = 1.0*4.5*VNCX_coeff  # [uA/uF] - 9 in rabbit
    Pd['KmCai'] = 3.59e-3    # [mM]
    Pd['KmCao'] = 1.3        # [mM]
    Pd['KmNai'] = 12.29      # [mM]
    Pd['KmNao'] = 87.5       # [mM]
    Pd['ksat'] = 0.32        # [none]  
    Pd['nu'] = 0.27          # [none]
    Pd['Kdact'] = 0.150e-3   # [mM] 
    Pd['Q10NCX'] = 1.57      # [none]
    Pd['IbarSLCaP'] = 0.0673 # IbarSLCaP FEI changed [uA/uF](2.2 umol/L cytosol/sec)[uA/uF]
    Pd['KmPCa'] = 0.5e-3     # [mM] 
    Pd['GCaB'] = 5.513e-4*GCaB_coeff    # [uA/uF] 3
    Pd['Q10SLCaP'] = 2.35    # [none]
    
    # SR flux parameters
    Pd['Q10SRCaP'] = 2.6          # [none]
    Pd['Vmax_SRCaP'] = 1.0*5.3114e-3  # [mM/msec] (286 umol/L cytosol/sec)
    Pd['Kmf'] = 0.246e-3          # [mM] default
    Pd['Kmr'] = 1.7               # [mM]L cytosol
    Pd['hillSRCaP'] = 1.787       # [mM]
    Pd['ks'] = 25                 # [1/ms]      
    Pd['koCa'] = 10               # [mM^-2 1/ms]   #default 10   modified 20
    Pd['kom'] = 0.06              # [1/ms]     
    Pd['kiCa'] = 0.5              # [1/mM/ms]
    Pd['kim'] = 0.005             # [1/ms]
    Pd['ec50SR'] = 0.45           # [mM]
    
    # Buffering parameters
    # koff: [1/s] = 1e-3*[1/ms];  kon: [1/uM/s] = [1/mM/ms]
    Pd['Bmax_Naj'] = 7.561       # [mM] # Bmax_Naj = 3.7; (c-code difference?)  # Na buffering
    Pd['Bmax_Nasl'] = 1.65       # [mM]
    Pd['koff_na'] = 1e-3         # [1/ms]
    Pd['kon_na'] = 0.1e-3        # [1/mM/ms]
    Pd['Bmax_TnClow'] = 70e-3    # [mM]                      # TnC low affinity
    Pd['koff_tncl'] = 19.6e-3    # [1/ms] 
    Pd['kon_tncl'] = 32.7        # [1/mM/ms]
    Pd['Bmax_TnChigh'] = 140e-3  # [mM]                      # TnC high affinity 
    Pd['koff_tnchca'] = 0.032e-3 # [1/ms] 
    Pd['kon_tnchca'] = 2.37      # [1/mM/ms]
    Pd['koff_tnchmg'] = 3.33e-3  # [1/ms] 
    Pd['kon_tnchmg'] = 3e-3      # [1/mM/ms]
    Pd['Bmax_CaM'] = 24e-3       # [mM] **? about setting to 0 in c-code**   # CaM buffering
    Pd['koff_cam'] = 238e-3      # [1/ms] 
    Pd['kon_cam'] = 34           # [1/mM/ms]
    Pd['Bmax_myosin'] = 140e-3   # [mM]                      # Myosin buffering
    Pd['koff_myoca'] = 0.46e-3   # [1/ms]
    Pd['kon_myoca'] = 13.8       # [1/mM/ms]
    Pd['koff_myomg'] = 0.057e-3  # [1/ms]
    Pd['kon_myomg'] = 0.0157     # [1/mM/ms]
    Pd['Bmax_SR'] = 19*.9e-3     # [mM] (Bers text says 47e-3) 19e-3
    Pd['koff_sr'] = 60e-3        # [1/ms]
    Pd['kon_sr'] = 100           # [1/mM/ms]
    Pd['Bmax_SLlowsl'] = 37.4e-3        # [mM]    # SL buffering
    Pd['Bmax_SLlowj'] = 4.6e-3*0.1    # [mM]    #Fei *0.1!!! junction reduction factor
    Pd['koff_sll'] = 1300e-3     # [1/ms]
    Pd['kon_sll'] = 100          # [1/mM/ms]
    Pd['Bmax_SLhighsl'] = 13.4e-3       # [mM] 
    Pd['Bmax_SLhighj'] = 1.65e-3*0.1  # [mM] #Fei *0.1!!! junction reduction factor
    Pd['koff_slh'] = 30e-3       # [1/ms]
    Pd['kon_slh'] = 100          # [1/mM/ms]
    Pd['Bmax_Csqn'] = 140e-3            # [mM] # Bmax_Csqn = 2.6;      # Csqn buffering
    Pd['koff_csqn'] = 65         # [1/ms] 
    Pd['kon_csqn'] = 100         # [1/mM/ms] 
    
    # Mark all states as dynamic ODEs:
    Pd['dynamic'] = [1]*39
 
    return Pd
 
 
#----------------------------------------------------------------------
# Define a default initial condition:
def Initialize(y0 = None):
     
    if y0 is None:
        mo = 1.405627e-3
        ho = 9.867005e-1
        jo = 9.915620e-1 
        do = 7.175662e-6 
        fo = 1.000681 
        fcaBjo = 2.421991e-2
        fcaBslo = 1.452605e-2
        xtoso = 4.051574e-3
        ytoso = 9.945511e-1 
        xtofo = 4.051574e-3 
        ytofo =  9.945511e-1 
        xkro = 8.641386e-3 
        xkso =  5.412034e-3
        RyRro = 8.884332e-1
        RyRoo = 8.156628e-7 
        RyRio = 1.024274e-7 
        NaBjo = 3.539892
        NaBslo = 7.720854e-1 
        TnCLo = 8.773191e-3 
        TnCHco = 1.078283e-1 
        TnCHmo = 1.524002e-2 
        CaMo = 2.911916e-4 
        Myoco = 1.298754e-3 
        Myomo = 1.381982e-1
        SRBo = 2.143165e-3 
        SLLjo = 9.566355e-3 
        SLLslo = 1.110363e-1 
        SLHjo = 7.347888e-3 
        SLHslo = 7.297378e-2 
        Csqnbo =  1.242988
        Ca_sro = 0.1e-1 
        Najo = 9.06
        Naslo = 9.06
        Naio = 9.06
        Kio = 120 
        Cajo = 1.737475e-4 
        Caslo =  1.031812e-4 
        Caio = 8.597401e-5 
        Vmo = -8.09763e+1 
             
        
        y0 = [mo, ho, jo, do, fo, fcaBjo, fcaBslo, xtoso, ytoso, xtofo,
              ytofo, xkro, xkso,RyRro, RyRoo, RyRio, NaBjo, NaBslo, TnCLo,
              TnCHco, TnCHmo, CaMo, Myoco, Myomo,SRBo, SLLjo, SLLslo, SLHjo,
              SLHslo, Csqnbo,Ca_sro, Najo, Naslo, Naio, Kio, Cajo, Caslo, Caio, Vmo]

        return y0 
    else:
        return y0
         
def name2index(name):
    """Take the name of a state in the model, return the index of that state in the solution vector y."""
    state_names = ["mo", "ho", "jo", "do", "fo", "fcaBjo", "fcaBslo", 
           "xtoso", "ytoso", "xtofo", "ytofo", "xkro", "xkso", "RyRro",
           "RyRoo", "RyRio", "NaBjo", "NaBslo", "TnCLo", "TnCHco", "TnCHmo",
           "CaMo", "Myoco", "Myomo", "SRBo", "SLLjo", "SLLslo", "SLHjo", 
           "SLHslo", "Csqnbo", "Ca_sro", "Najo", "Naslo", "Naio", "Kio", 
           "Cajo", "Caslo", "Caio", "Vmo"]
    if type(name) == str:
        try:
            return state_names.index(name)
        except ValueError:
            raise ValueError("{} is not a state in the model".format(name))
    else:
        raise TypeError("Input must be the name of a state in the model as a str")
 
def index2name(index):
    state_names = ["mo", "ho", "jo", "do", "fo", "fcaBjo", "fcaBslo", 
           "xtoso", "ytoso", "xtofo", "ytofo", "xkro", "xkso", "RyRro",
           "RyRoo", "RyRio", "NaBjo", "NaBslo", "TnCLo", "TnCHco", "TnCHmo",
           "CaMo", "Myoco", "Myomo", "SRBo", "SLLjo", "SLLslo", "SLHjo", 
           "SLHslo", "Csqnbo", "Ca_sro", "Najo", "Naslo", "Naio", "Kio", 
           "Cajo", "Caslo", "Caio", "Vmo"]
    if type(index) == int:
        return state_names[index]
    else:
        raise TypeError("Input must be the index of a state as an int")
#--------------------------------------------------------------------------------------------     

def grandi_bers_rhs_atrial(y, t, Pd):

    m,     h,     j,     d,     f,     fcaBj,     fcaBsl,    xtof,     ytof,     xkr,     xks,     RyRr,    RyRo,    RyRi,    NaBj,    NaBsl,    TnCL,     TnCHc,    TnCHm,    CaM,     Myoc,     Myom,     SRB,     SLLj,     SLLsl,     SLHj,     SLHsl,     Csqnb,     Ca_sr,    Naj,     Nasl,     Nai,     Ki,     Caj,     Casl,    Cai,     Vm,     rkuro,    skuro,    ml,    hl,    INal = y

    # Constants
    R = Pd['R']
    Frdy = Pd['Frdy']
    Temp = Pd['Temp']
    FoRT = Frdy/R/Temp
    Qpow = (Temp-310)/10
    Cmem = Pd['Cmem']
    
    # Cell geometry
    Vcell = pi*Pd['cellRadius']**2*Pd['cellLength']*1e-15 
    Vmyo = Pd['Vmyo_ratio']*Vcell
    Vsr = Pd['Vsr_ratio']*Vcell
    Vsl = Pd['Vsl_ratio']*Vcell
    Vjunc = Pd['Vjunc_ratio']*Vcell
    
    # Fractional currents in compartments
    Fjunc = Pd['Fjunc']
    Fsl = 1-Fjunc
    Fjunc_CaL = Pd['Fjunc_CaL'] 
    Fsl_CaL = 1-Fjunc_CaL

    # Fixed ion concentrations     
    Cli = Pd['Cli']
    Clo = Pd['Clo']
    Ko = Pd['Ko']
    Nao = Pd['Nao']
    Cao = Pd['Cao']
    Mgi = Pd['Mgi']

    # Buffering parameters
    # koff: [1/s] = 1e-3*[1/ms]  kon: [1/uM/s] = [1/mM/ms]
    Bmax_Naj = Pd['Bmax_Naj']
    Bmax_Nasl = Pd['Bmax_Nasl']
    koff_na = Pd['koff_na']
    kon_na = Pd['kon_na']
    Bmax_TnClow = Pd['Bmax_TnClow']
    koff_tncl = Pd['koff_tncl']
    kon_tncl = Pd['kon_tncl'] 
    Bmax_TnChigh = Pd['Bmax_TnChigh']
    koff_tnchca = Pd['koff_tnchca']
    kon_tnchca = Pd['kon_tnchca'] 
    koff_tnchmg = Pd['koff_tnchmg']
    kon_tnchmg = Pd['kon_tnchmg'] 
    Bmax_CaM = Pd['Bmax_CaM'] 
    koff_cam = Pd['koff_cam'] 
    kon_cam = Pd['kon_cam'] 
    Bmax_myosin = Pd['Bmax_myosin']
    koff_myoca = Pd['koff_myoca']
    kon_myoca = Pd['kon_myoca']
    koff_myomg = Pd['koff_myomg']
    kon_myomg = Pd['kon_myomg']
    Bmax_SR = Pd['Bmax_SR']
    koff_sr = Pd['koff_sr']
    kon_sr = Pd['kon_sr']
    Bmax_SLlowsl = Pd['Bmax_SLlowsl']*Vmyo/Vsl        # [mM]    # SL buffering
    Bmax_SLlowj = Pd['Bmax_SLlowj']*Vmyo/Vjunc    # [mM]   
    koff_sll = Pd['koff_sll']    # [1/ms]
    kon_sll = Pd['kon_sll']          # [1/mM/ms]
    Bmax_SLhighsl = Pd['Bmax_SLhighsl']*Vmyo/Vsl       # [mM] 
    Bmax_SLhighj = Pd['Bmax_SLhighj']*Vmyo/Vjunc  # [mM] 
    koff_slh = Pd['koff_slh']      # [1/ms]
    kon_slh = Pd['kon_slh']         # [1/mM/ms]
    Bmax_Csqn = Pd['Bmax_Csqn']*Vmyo/Vsr  # [mM] # Bmax_Csqn = 2.6      # Csqn buffering
    koff_csqn = Pd['koff_csqn']
    kon_csqn = Pd['kon_csqn']

    #########################33

    # Nernst Potentials
    ena_junc = (1/FoRT)*log(Nao/Naj)    # [mV]
    ena_sl = (1/FoRT)*log(Nao/Nasl)       # [mV]
    ek = (1/FoRT)*log(Ko/Ki)	        # [mV]
    eca_junc = (1/FoRT/2)*log(Cao/Caj)   # [mV]
    eca_sl = (1/FoRT/2)*log(Cao/Casl)     # [mV]
    ecl = (1/FoRT)*log(Cli/Clo)            # [mV]

    #CURRENTS
    #ten Tusscher formulation
    mss = 1 / ((1 + exp( -(56.86 + Vm) / 9.03 ))**2)
    taum = 0.1292 * exp(-((Vm+45.79)/15.54)**2) + 0.06487 * exp(-((Vm-4.823)/51.12)**2)                 
    ah = 0.0 if (Vm >= -40) else (0.057 * exp( -(Vm + 80) / 6.8 )) 
    bh =  (0.77 / (0.13*(1 + exp( -(Vm + 10.66) / 11.1 )))) if (Vm >= -40) else ((2.7 * exp( 0.079 * Vm) + 3.1*10**5 * exp(0.3485 * Vm))) 
    tauh = 1 / (ah + bh) 
    hss = 1 / ((1 + exp( (Vm + 71.55)/7.43 ))**2)
    aj = (0) if (Vm >= -40) else (((-2.5428 * 10**4*exp(0.2444*Vm) - 6.948*10**-6 * exp(-0.04391*Vm)) * (Vm + 37.78)) /(1 + exp( 0.311 * (Vm + 79.23) )))
    bj =  ((0.6 * exp( 0.057 * Vm)) / (1 + exp( -0.1 * (Vm + 32) ))) if (Vm >= -40) else ((0.02424 * exp( -0.01052 * Vm )) / (1 + exp( -0.1378 * (Vm + 40.14) ))) 
    tauj = 1 / (aj + bj)
    jss = 1 / ((1 + exp( (Vm + 71.55)/7.43 ))**2)         
    d_m = (mss - m) / taum
    d_h = (hss - h) / tauh
    d_j = (jss - j) / tauj
    I_Na_junc = Fjunc*Pd['GNa']*m**3*h*j*(Vm-ena_junc)
    I_Na_sl = Fsl*Pd['GNa']*m**3*h*j*(Vm-ena_sl)
    I_Na = I_Na_junc+I_Na_sl

    # Late I_Na
    aml = 0.32*(Vm+47.13)/(1-exp(-0.1*(Vm+47.13)))
    bml = 0.08*exp(-Vm/11)
    hlinf = 1/(1.0+exp((Vm+91.0)/6.1))
    d_ml = aml*(1-ml)-bml*ml
    d_hl = (hlinf-hl)/Pd['tauhl']
    I_NaL_junc = Pd['Fjunc']*Pd['GNaL']*ml**3*hl*(Vm-ena_junc)
    I_NaL_sl = Fsl*Pd['GNaL']*ml**3*hl*(Vm-ena_sl)
    I_NaL = I_NaL_junc + I_NaL_sl
    d_INal = I_NaL

    # I_nak: Na/K Pump Current
    sigma = (exp(Nao/67.3)-1)/7
    fnak = 1/(1+0.1245*exp(-0.1*Vm*FoRT)+0.0365*sigma*exp(-Vm*FoRT))
    I_nak_junc = 1*Fjunc*Pd['IbarNaK']*fnak*Ko/(1+(Pd['KmNaip']/Naj)**4)/(Ko+Pd['KmKo'])
    I_nak_sl = 1*Fsl*Pd['IbarNaK']*fnak*Ko/(1+(Pd['KmNaip']/Nasl)**4)/(Ko+Pd['KmKo'])
    I_nak = I_nak_junc+I_nak_sl

    ## I_kr: Rapidly Activating K Current
    gkr = Pd['Gkr']*sqrt(Ko/5.4)
    xrss = 1/(1+exp(-(Vm+10)/5))
    tauxr = 550/(1+exp((-22-Vm)/9))*6/(1+exp((Vm-(-11))/9))+230/(1+exp((Vm-(-40))/20))
    d_xkr = (xrss-xkr)/tauxr
    rkr = 1/(1+exp((Vm+74)/24))
    I_kr = gkr*xkr*rkr*(Vm-ek)

    ## I_ks: Slowly Activating K Current
    eks = (1/FoRT)*log((Ko+Pd['pNaK']*Nao)/(Ki+Pd['pNaK']*Nai))
    gks_junc=1*(1+1*Pd['AF']+2*Pd['ISO'])*Pd['Gks']
    gks_sl=1*(1+1*Pd['AF']+2*Pd['ISO'])*Pd['Gks'] #FRA
    xsss = 1 / (1+exp(-(Vm + 40*Pd['ISO'] + 3.8)/14.25)) # fitting Fra
    tauxs=990.1/(1+exp(-(Vm+40*Pd['ISO']+2.436)/14.12))
    d_xks = (xsss-xks)/tauxs
    I_ks_junc = Fjunc*Pd['Gks']*xks**2*(Vm-eks)
    I_ks_sl = Fsl*Pd['Gks']*xks**2*(Vm-eks)    
    I_ks = I_ks_junc+I_ks_sl

    #I_kp: Plateau K current
    kp_kp = 1/(1+exp(7.488-Vm/5.98))
    I_kp_junc = Fjunc*Pd['Gkp']*kp_kp*(Vm-ek)
    I_kp_sl = Fsl*Pd['Gkp']*kp_kp*(Vm-ek)
    I_kp = I_kp_junc+I_kp_sl

    ## I_to: Transient Outward K Current
    I_tof = Pd['GtoFast']*xtof*ytof*(Vm-ek)
    xtoss = 1/(1+exp(-(Vm-1.0)/11.0))
    ytoss = 1/(1+exp((Vm+40.5)/11.5))
    tauxtof = 3.5*exp(-((Vm+45)/30)**2)+1.5 #***F97C TESTING***
    tauytof = 25.635*exp(-(((Vm+52.45)/15.8827)**2.0))+24.14
    d_xtof = (xtoss-xtof)/tauxtof
    d_ytof = (ytoss-ytof)/tauytof
    I_to = I_tof

    ## I_kur: Ultra rapid delayed rectifier Outward K Current
    xkurss = ( 1.0/ ( 1.0 + exp((Vm+6.0)/-8.6)))
    tauxkur = 9.0/(1.0+exp((Vm+5.0)/12.0))+0.5
    ykurss = ( (1.0)/ ( 1.0 + exp( (Vm+7.5)/10.0 )))
    tauykur = 590.0/(1.0+exp((Vm+60.0)/10.0))+3050.0
    d_rkuro = (xkurss-rkuro)/tauxkur
    d_skuro = (ykurss-skuro)/tauykur
    I_kur = 1*Pd['Gkur']*rkuro*skuro*(Vm-ek)

    ## I_ki: Time-Independent K Current
    aki = 1.02/(1+exp(0.2385*(Vm-ek-59.215)))
    bki =(0.49124*exp(0.08032*(Vm+5.476-ek)) + exp(0.06175*(Vm-ek-594.31))) /(1 + exp(-0.5143*(Vm-ek+4.753)))
    kiss = aki/(aki+bki)
    I_ki =Pd['Gki']*sqrt(Ko/5.4)*kiss*(Vm-ek)
    
    ## I_kAch: Acetylcholine sensitive K+ current
    I_kAch = Pd['GkAch']*(0.08+0.4/(1+exp((Vm+91)/12)))*(Vm-ek);

    # I_ClCa: Ca-activated Cl Current
    I_ClCa_junc = Fjunc*Pd['GClCa']/(1+Pd['KdClCa']/Caj)*(Vm-ecl)
    I_ClCa_sl = Fsl*Pd['GClCa']/(1+Pd['KdClCa']/Casl)*(Vm-ecl)
    I_ClCa = I_ClCa_junc+I_ClCa_sl
 
    # I_Catot = I_Ca+I_CaK+I_CaNa
    ## I_Ca: L-type Calcium Current
    fss = 1/(1+exp((Vm+35)/9))+0.6/(1+exp((50-Vm)/20))
    dss = 1/(1+exp(-(Vm+3*Pd['ISO']+9)/6.0))
    taud = dss*(1-exp(-(Vm+3*Pd['ISO']+9)/6.0))/(0.035*(Vm+3*Pd['ISO']+9))
    tauf = 1/(0.0197*exp( -(0.0337*(Vm+3*Pd['ISO']+25))**2 )+0.02)
    d_d = (dss-d)/taud
    d_f = (fss-f)/tauf
    d_fcaBj = 1.7*Caj*(1-fcaBj)-11.9e-3*fcaBj # fCa_junc   koff!!!!!!!!
    d_fcaBsl = 1.7*Casl*(1-fcaBsl)-11.9e-3*fcaBsl # fCa_sl
    fcaCaMSL= 0.1/(1+(0.01/Casl))
    fcaCaj= 0.1/(1+(0.01/Caj))
    fcaCaMSL=0
    fcaCaj= 0
    ibarca_j = Pd['pCa']*4*(Vm*Frdy*FoRT) * (0.341*Caj*exp(2*Vm*FoRT)-0.341*Cao) /(exp(2*Vm*FoRT)-1)
    ibarca_sl = Pd['pCa']*4*(Vm*Frdy*FoRT) * (0.341*Casl*exp(2*Vm*FoRT)-0.341*Cao) /(exp(2*Vm*FoRT)-1)
    ibark = Pd['pK']*(Vm*Frdy*FoRT)*(0.75*Ki*exp(Vm*FoRT)-0.75*Ko) /(exp(Vm*FoRT)-1)
    ibarna_j = Pd['pNa']*(Vm*Frdy*FoRT) *(0.75*Naj*exp(Vm*FoRT)-0.75*Nao)  /(exp(Vm*FoRT)-1)
    ibarna_sl = Pd['pNa']*(Vm*Frdy*FoRT) *(0.75*Nasl*exp(Vm*FoRT)-0.75*Nao)  /(exp(Vm*FoRT)-1)
    I_Ca_junc = (Fjunc_CaL*ibarca_j*d*f*((1-fcaBj)+fcaCaj)*Pd['Q10CaL']**Qpow)*0.45*1
    I_Ca_sl = (Fsl_CaL*ibarca_sl*d*f*((1-fcaBsl)+fcaCaMSL)*Pd['Q10CaL']**Qpow)*0.45*1
    I_Ca = I_Ca_junc+I_Ca_sl
    I_CaK = (ibark*d*f*(Fjunc_CaL*(fcaCaj+(1-fcaBj))+Fsl_CaL*(fcaCaMSL+(1-fcaBsl)))*Pd['Q10CaL']**Qpow)*0.45*1
    I_CaNa_junc = (Fjunc_CaL*ibarna_j*d*f*((1-fcaBj)+fcaCaj)*Pd['Q10CaL']**Qpow)*0.45*1
    I_CaNa_sl = (Fsl_CaL*ibarna_sl*d*f*((1-fcaBsl)+fcaCaMSL)*Pd['Q10CaL']**Qpow)*.45*1
    I_CaNa = I_CaNa_junc+I_CaNa_sl
    I_Catot = I_Ca+I_CaK+I_CaNa

    # I_ncx: Na/Ca Exchanger flux
    Ka_junc = 1/(1+(Pd['Kdact']/Caj)**2)
    Ka_sl = 1/(1+(Pd['Kdact']/Casl)**2)
    s1_junc = exp(Pd['nu']*Vm*FoRT)*Naj**3*Cao
    s1_sl = exp(Pd['nu']*Vm*FoRT)*Nasl**3*Cao
    s2_junc = exp((Pd['nu']-1)*Vm*FoRT)*Nao**3*Caj
    s3_junc = Pd['KmCai']*Nao**3*(1+(Naj/Pd['KmNai'])**3) + Pd['KmNao']**3*Caj*(1+Caj/Pd['KmCai'])+Pd['KmCao']*Naj**3+Naj**3*Cao+Nao**3*Caj
    s2_sl = exp((Pd['nu']-1)*Vm*FoRT)*Nao**3*Casl
    s3_sl = Pd['KmCai']*Nao**3*(1+(Nasl/Pd['KmNai'])**3) + Pd['KmNao']**3*Casl*(1+Casl/Pd['KmCai'])+Pd['KmCao']*Nasl**3+Nasl**3*Cao+Nao**3*Casl
    I_ncx_junc = Fjunc*Pd['IbarNCX']*Pd['Q10NCX']**Qpow*Ka_junc*(s1_junc-s2_junc)/s3_junc/(1+Pd['ksat']*exp((Pd['nu']-1)*Vm*FoRT))
    I_ncx_sl = Fsl*Pd['IbarNCX']*Pd['Q10NCX']**Qpow*Ka_sl*(s1_sl-s2_sl)/s3_sl/(1+Pd['ksat']*exp((Pd['nu']-1)*Vm*FoRT))
    I_ncx = I_ncx_junc+I_ncx_sl

    # I_pca: Sarcolemmal Ca Pump Current
    I_pca_junc = Fjunc*Pd['Q10SLCaP']**Qpow*Pd['IbarSLCaP']*Caj**1.6/(Pd['KmPCa']**1.6+Caj**1.6)
    I_pca_sl = Fsl*Pd['Q10SLCaP']**Qpow*Pd['IbarSLCaP']*Casl**1.6/(Pd['KmPCa']**1.6+Casl**1.6)
    I_pca = I_pca_junc+I_pca_sl

    ## SR fluxes: Calcium Release, SR Ca pump, SR Ca leak
    MaxSR = 15 
    MinSR = 1
    kCaSR = MaxSR - (MaxSR-MinSR)/(1+(Pd['ec50SR']/Ca_sr)**2.5)
    koSRCa = Pd['koCa']/kCaSR
    kiSRCa = Pd['kiCa']*kCaSR
    RI = 1-RyRr-RyRo-RyRi
    d_RyRr = (Pd['kim']*RI-kiSRCa*Caj*RyRr)-(koSRCa*Caj**2*RyRr-Pd['kom']*RyRo)   # R
    d_RyRo = (koSRCa*Caj**2*RyRr-Pd['kom']*RyRo)-(kiSRCa*Caj*RyRo-Pd['kim']*RyRi)# O
    d_RyRi = (kiSRCa*Caj*RyRo-Pd['kim']*RyRi)-(Pd['kom']*RyRi-koSRCa*Caj**2*RI)   # I
    J_SRCarel = Pd['ks']*RyRo*(Ca_sr-Caj)          # [mM/ms]
    J_serca = 1*Pd['Q10SRCaP']**Qpow*Pd['Vmax_SRCaP']*((Cai/Pd['Kmf'])**Pd['hillSRCaP']-(Ca_sr/Pd['Kmr'])**Pd['hillSRCaP'])/(1+(Cai/Pd['Kmf'])**Pd['hillSRCaP']+(Ca_sr/Pd['Kmr'])**Pd['hillSRCaP'])
    J_SRleak = (1.0+0.25*Pd['AF'])*5.348e-6*(Ca_sr-Caj)           #   [mM/ms]
    
    # BACKROUND CURRENTS
    # I_nabk: Na Background Current
    I_nabk_junc = Fjunc*Pd['GNaB']*(Vm-ena_junc)
    I_nabk_sl = Fsl*Pd['GNaB']*(Vm-ena_sl)
    I_nabk = I_nabk_junc+I_nabk_sl    # I_nabk: Na Background Current
    I_nabk_junc = Fjunc*Pd['GNaB']*(Vm-ena_junc)
    I_nabk_sl = Fsl*Pd['GNaB']*(Vm-ena_sl)
    I_nabk = I_nabk_junc+I_nabk_sl
    
    # I_cabk: Ca Background Current
    I_cabk_junc = Fjunc*Pd['GCaB']*(Vm-eca_junc)
    I_cabk_sl = Fsl*Pd['GCaB']*(Vm-eca_sl)
    I_cabk = I_cabk_junc+I_cabk_sl
    
    # I_Clbk: Chloride Background Current
    I_Clbk = Pd['GClB']*(Vm-ecl)

    ## Sodium and Calcium Buffering
    d_NaBj = kon_na*Naj*(Bmax_Naj-NaBj)-koff_na*NaBj        # NaBj      [mM/ms]
    d_NaBsl = kon_na*Nasl*(Bmax_Nasl-NaBsl)-koff_na*NaBsl       # NaBsl     [mM/ms]

    # Cytosolic Ca Buffers
    d_TnCL = kon_tncl*Cai*(Bmax_TnClow-TnCL)-koff_tncl*TnCL            # TnCL      [mM/ms]
    d_TnCHc = kon_tnchca*Cai*(Bmax_TnChigh-TnCHc-TnCHm)-koff_tnchca*TnCHc # TnCHc     [mM/ms]
    d_TnCHm = kon_tnchmg*Mgi*(Bmax_TnChigh-TnCHc-TnCHm)-koff_tnchmg*TnCHm   # TnCHm     [mM/ms]
    d_CaM = kon_cam*Cai*(Bmax_CaM-CaM)-koff_cam*CaM                 # CaM       [mM/ms]
    d_Myoc = kon_myoca*Cai*(Bmax_myosin-Myoc-Myom)-koff_myoca*Myoc    # Myosin_ca [mM/ms]
    d_Myom = kon_myomg*Mgi*(Bmax_myosin-Myoc-Myom)-koff_myomg*Myom      # Myosin_mg [mM/ms]
    d_SRB = kon_sr*Cai*(Bmax_SR-SRB)-koff_sr*SRB                    # SRB       [mM/ms]
    J_CaB_cytosol = d_TnCL + d_TnCHc + d_TnCHm + d_CaM + d_Myoc + d_Myom + d_SRB

    # Junctional and SL Ca Buffers
    d_SLLj = kon_sll*Caj*(Bmax_SLlowj-SLLj)-koff_sll*SLLj       # SLLj      [mM/ms]
    d_SLLsl = kon_sll*Casl*(Bmax_SLlowsl-SLLsl)-koff_sll*SLLsl      # SLLsl     [mM/ms]
    d_SLHj = kon_slh*Caj*(Bmax_SLhighj-SLHj)-koff_slh*SLHj      # SLHj      [mM/ms]
    d_SLHsl = kon_slh*Casl*(Bmax_SLhighsl-SLHsl)-koff_slh*SLHsl     # SLHsl     [mM/ms]
    J_CaB_junction = d_SLLj+d_SLHj
    J_CaB_sl = d_SLLsl+d_SLHsl

    ## Ion concentrations
    # SR Ca Concentrations
    d_Csqnb = kon_csqn*Ca_sr*(Bmax_Csqn-Csqnb)-koff_csqn*Csqnb       # Csqn      [mM/ms]
    d_Ca_sr = J_serca-(J_SRleak*Vmyo/Vsr+J_SRCarel)-d_Csqnb         # Ca_sr     [mM/ms] #Ratio 3 leak current
    # d_Ca_sr=0

    # Sodium Concentrations
    I_Na_tot_junc = I_Na_junc+I_nabk_junc+3*I_ncx_junc+3*I_nak_junc+I_CaNa_junc+I_NaL_junc   # [uA/uF]
    I_Na_tot_sl = I_Na_sl+I_nabk_sl+3*I_ncx_sl+3*I_nak_sl+I_CaNa_sl+I_NaL_sl   # [uA/uF]
    I_Na_tot_sl2 = 3*I_ncx_sl+3*I_nak_sl+I_CaNa_sl   # [uA/uF]
    I_Na_tot_junc2 = 3*I_ncx_junc+3*I_nak_junc+I_CaNa_junc   # [uA/uF]
    d_Naj = -I_Na_tot_junc*Cmem/(Vjunc*Frdy)+Pd['J_na_juncsl']/Vjunc*(Nasl-Naj)-d_NaBj
    d_Nasl = -I_Na_tot_sl*Cmem/(Vsl*Frdy)+Pd['J_na_juncsl']/Vsl*(Naj-Nasl)+Pd['J_na_slmyo']/Vsl*(Nai-Nasl)-d_NaBsl

    #FluxNaSL=d_Nasl
    d_Nai = Pd['J_na_slmyo']/Vmyo*(Nasl-Nai)             # [mM/msec] 

    # Potassium Concentration
    I_K_tot = I_to+I_kr+I_ks+I_ki-2*I_nak+I_CaK+I_kp+I_kur+I_kAch     # [uA/uF]
    d_Ki =0 # -I_K_tot*Cmem/(Vmyo*Frdy)

    # Calcium Concentrations
    I_Ca_tot_junc = I_Ca_junc+I_cabk_junc+I_pca_junc-2*I_ncx_junc                   # [uA/uF]
    I_Ca_tot_sl = I_Ca_sl+I_cabk_sl+I_pca_sl-2*I_ncx_sl            # [uA/uF]
    d_Caj = -I_Ca_tot_junc*Cmem/(Vjunc*2*Frdy)+Pd['J_ca_juncsl']/Vjunc*(Casl-Caj)   -J_CaB_junction+(J_SRCarel)*Vsr/Vjunc+J_SRleak*Vmyo/Vjunc  # Ca_j
    d_Casl = -I_Ca_tot_sl*Cmem/(Vsl*2*Frdy)+Pd['J_ca_juncsl']/Vsl*(Caj-Casl)  + Pd['J_ca_slmyo']/Vsl*(Cai-Casl)-J_CaB_sl   # Ca_sl
    d_Cai = -J_serca*Vsr/Vmyo-J_CaB_cytosol +Pd['J_ca_slmyo']/Vmyo*(Casl-Cai)

    ## Summing the current components
    I_Na_tot = I_Na_tot_junc + I_Na_tot_sl          # [uA/uF]
    I_Cl_tot = I_ClCa+I_Clbk                        # [uA/uF]
    I_Ca_tot = I_Ca_tot_junc+I_Ca_tot_sl
    I_tot = I_Na_tot+I_Cl_tot+I_Ca_tot+I_K_tot
    I_app = Pd['I_app'] if (t<5) else 0.0
    d_Vm = -(I_tot-I_app)

    ydot = [d_m,d_h, d_j, d_d, d_f,d_fcaBj, d_fcaBsl, d_xtof, d_ytof, d_xkr, d_xks, d_RyRr, d_RyRo, d_RyRi, d_NaBj, d_NaBsl, d_TnCL, d_TnCHc, d_TnCHm, d_CaM, d_Myoc, d_Myom, d_SRB, d_SLLj, d_SLLsl, d_SLHj, d_SLHsl, d_Csqnb, d_Ca_sr, d_Naj, d_Nasl, d_Nai, d_Ki, d_Caj, d_Casl, d_Cai, d_Vm,  d_rkuro, d_skuro, d_ml, d_hl, d_INal]
    
    ydot = list(map(lambda x,y:x*y, ydot, Pd['dynamic']))

    return ydot

#---------------------------------------------------------------------------------

def set_Pd_atrial(Params_to_change = None):
     
    if Params_to_change is None:
        GNa_coeff = 1
        GtoFast_coeff = 1
        Gkr_coeff = 1
        Gkur_coeff = 1
        Gks_coeff = 1
        Gkp_coeff = 1
        Gk1_coeff = 1
        GClCa_coeff = 1
        pCa_coeff = 1
        VNCX_coeff = 1
        VNaK_coeff = 1
        GNaB_coeff = 1
        GCaB_coeff = 1
        GClB_coeff = 1
        GkAch_coeff = 1
        Ach = 0
    else:
        GNa_coeff = Params_to_change[0]
        GtoFast_coeff = Params_to_change[1]
        Gkr_coeff = Params_to_change[2]
        Gkur_coeff = Params_to_change[3]
        Gks_coeff = Params_to_change[4]
        Gkp_coeff = Params_to_change[5]
        Gk1_coeff = Params_to_change[6]
        GClCa_coeff = Params_to_change[7]
        pCa_coeff = Params_to_change[8]
        VNCX_coeff = Params_to_change[9]
        VNaK_coeff = Params_to_change[10]
        GNaB_coeff = Params_to_change[11]
        GCaB_coeff = Params_to_change[12]
        GClB_coeff = Params_to_change[13]
        GkAch_coeff = Params_to_change[14]
        Ach = Params_to_change[15]
     
    Pd = {}
    
    #Pacing current
    Pd['I_app'] = 12.5
    
    ## EPI or ENDO?
    Pd['epi']=1
    
    ## AF
    Pd['AF'] = 0
    
    ## ISO
    Pd['ISO'] = 0
    
    ## Ach
    Pd['Ach'] = Ach
    
    ## Right Atrium
    Pd['RA'] = 0
    
    # Constants
    Pd['R'] = 8314       # [J/kmol*K]  
    Pd['Frdy'] = 96485   # [C/mol]  
    Pd['Temp'] = 310     # [K]
    Pd['Cmem'] = 1.10e-10   # [F] membrane capacitance
    
    # Cell geometry
    Pd['cellLength'] = 100     # cell length [um]
    Pd['cellRadius'] = 10.25   # cell radius [um]
    Pd['Vmyo_ratio'] = 0.65
    Pd['Vsr_ratio'] = 0.035
    Pd['Vsl_ratio'] = 0.02
    Pd['Vjunc_ratio'] = 0.00539
    
    #Intercompartmental fluxes
    Pd['J_ca_juncsl'] =1/1.2134e12 # [L/msec] = 8.2413e-13
    Pd['J_ca_slmyo'] = 1/2.68510e11 # [L/msec] = 3.2743e-12
    Pd['J_na_juncsl'] = 1/(1.6382e12/3*100) # [L/msec] = 6.1043e-13
    Pd['J_na_slmyo'] = 1/(1.8308e10/3*100)  # [L/msec] = 5.4621e-11
    
    # Fractional currents in compartments
    Pd['Fjunc'] = 0.11   
    Pd['Fjunc_CaL'] = 0.9 
    
    # Fixed ion concentrations     
    Pd['Cli'] = 15   # Intracellular Cl  [mM]
    Pd['Clo'] = 150  # Extracellular Cl  [mM]
    Pd['Ko']= 5.4   # Extracellular K   [mM]
    Pd['Nao'] = 140  # Extracellular Na  [mM]
    Pd['Cao'] = 1.8  # Extracellular Ca  [mM]1.8
    Pd['Mgi'] = 1    # Intracellular Mg  [mM]
    
    # Na transport parameters
    Pd['GNa']=10*(1-0.1*Pd['AF'])*GNa_coeff
    Pd['GNaB'] = 0.597e-3*GNaB_coeff    # [mS/uF] 
    Pd['IbarNaK'] = 1.26*VNaK_coeff      # [uA/uF]
    Pd['KmNaip'] = 11*(1-0.25*Pd['ISO'])         # [mM]11
    Pd['KmKo'] =1.5         # [mM]1.5
    Pd['Q10NaK'] = 1.63  
    Pd['Q10KmNai'] = 1.39
    
    ## K current parameters
    Pd['pNaK'] = 0.01833      
    Pd['Gkp'] = 0.002*Gkp_coeff
    Pd['Gkr'] = 0.035*sqrt(Pd['Ko']/5.4)*Gkr_coeff
    Pd['Gki'] = (1+1*Pd['AF'])*0.0525*Gk1_coeff
    Pd['Gks'] = 0.0035*Gks_coeff
    Pd['GtoFast'] = (1.0-0.7*Pd['AF'])*0.165*1.0*GtoFast_coeff #nS/pF
    Pd['Gkur'] = 1*(1.0-0.5*Pd['AF'])*(1+2*Pd['ISO'])* 0.045*(1+0.2*Pd['RA'])*Gkur_coeff #nS/pF maleckar 0.045
    Pd['GkAch'] = (1/(1+(0.03/(Pd['Ach']+1e-05))**2.1))*GkAch_coeff
    
    # Cl current parameters
    Pd['GClCa'] =0.0548*GClCa_coeff   # [mS/uF]
    Pd['GClB'] = 9e-3*GClB_coeff        # [mS/uF]
    Pd['KdClCa'] = 100e-3    # [mM]
    
    # I_Ca parameters
    Pd['pNa'] = (1+0.5*Pd['ISO'])*(1-0.5*Pd['AF'])*0.75e-8     # [cm/sec]
    Pd['pCa'] = (1+0.5*Pd['ISO'])*(1-0.5*Pd['AF'])*2.7e-4*pCa_coeff     # [cm/sec]
    Pd['pK'] = (1+0.5*Pd['ISO'])*(1-0.5*Pd['AF'])*1.35e-7      # [cm/sec]
    Pd['Q10CaL'] = 1.8       
    
    ## Ca transport parameters
    Pd['IbarNCX'] = (1+0.4*Pd['AF'])*3.15*VNCX_coeff    # [uA/uF]5.5 before - 9 in rabbit
    Pd['KmCai'] = 3.59e-3              # [mM]
    Pd['KmCao'] = 1.3                  # [mM]
    Pd['KmNai'] = 12.29                # [mM]
    Pd['KmNao'] = 87.5                 # [mM]
    Pd['ksat'] = 0.27                  # [none]  
    Pd['nu'] = 0.35                    # [none]
    Pd['Kdact'] = 0.384e-3             # [mM] 
    Pd['Q10NCX'] = 1.57                # [none]
    Pd['IbarSLCaP'] = 0.0471           # IbarSLCaP FEI changed [uA/uF](2.2 umol/L cytosol/sec) jeff 0.093 [uA/uF]
    Pd['KmPCa'] = 0.5e-3               # [mM] 
    Pd['GCaB'] = 6.0643e-4*GCaB_coeff             # [uA/uF] 3
    Pd['Q10SLCaP'] = 2.35              # [none]
    
    # SR flux parameters
    Pd['Q10SRCaP'] = 2.6                       # [none]
    Pd['Vmax_SRCaP'] = 5.3114e-3           # [mM/msec] (286 umol/L cytosol/sec)
    Pd['Kmf'] = (2.5-1.25*Pd['ISO'])*0.246e-3        # [mM] default
    Pd['Kmr'] = 1.7                            # [mM]L cytosol
    Pd['hillSRCaP'] = 1.787                    # [mM]
    Pd['ks'] = 25                              # [1/ms]      
    Pd['koCa'] = 10+20*Pd['AF']+10*Pd['ISO']*(1-Pd['AF'])        # [mM^-2 1/ms]   #default 10   modified 20
    Pd['kom'] = 0.06                           # [1/ms]     
    Pd['kiCa'] = 0.5                           # [1/mM/ms]
    Pd['kim'] = 0.005                          # [1/ms]
    Pd['ec50SR'] = 0.45                        # [mM]
    
    # Buffering parameters
    # koff: [1/s] = 1e-3*[1/ms]  kon: [1/uM/s] = [1/mM/ms]
    Pd['Bmax_Naj'] = 7.561                 # [mM] # Bmax_Naj = 3.7 (c-code difference?)  # Na buffering
    Pd['Bmax_Nasl'] = 1.65                 # [mM]
    Pd['koff_na'] = 1e-3                   # [1/ms]
    Pd['kon_na'] = 0.1e-3                  # [1/mM/ms]
    Pd['Bmax_TnClow'] = 70e-3              # [mM]                      # TnC low affinity
    Pd['koff_tncl'] = (1+0.8*Pd['ISO'])*19.6e-3  # [1/ms] 
    Pd['kon_tncl'] = 32.7                  # [1/mM/ms]
    Pd['Bmax_TnChigh'] = 140e-3            # [mM]                      # TnC high affinity 
    Pd['koff_tnchca'] = 0.032e-3           # [1/ms] 
    Pd['kon_tnchca'] = 2.37                # [1/mM/ms]
    Pd['koff_tnchmg'] = 3.33e-3            # [1/ms] 
    Pd['kon_tnchmg'] = 3e-3                # [1/mM/ms]
    Pd['Bmax_CaM'] = 24e-3                 # [mM] **? about setting to 0 in c-code**   # CaM buffering
    Pd['koff_cam'] = 238e-3                # [1/ms] 
    Pd['kon_cam'] = 34                     # [1/mM/ms]
    Pd['Bmax_myosin'] = 140e-3             # [mM]                      # Myosin buffering
    Pd['koff_myoca'] = 0.46e-3             # [1/ms]
    Pd['kon_myoca'] = 13.8                 # [1/mM/ms]
    Pd['koff_myomg'] = 0.057e-3            # [1/ms]
    Pd['kon_myomg'] = 0.0157               # [1/mM/ms]
    Pd['Bmax_SR'] = 19*.9e-3               # [mM] (Bers text says 47e-3) 19e-3
    Pd['koff_sr'] = 60e-3                  # [1/ms]
    Pd['kon_sr'] = 100                     # [1/mM/ms]
    Pd['Bmax_SLlowsl'] = 37.4e-3           # [mM]    # SL buffering
    Pd['Bmax_SLlowj'] = 4.6e-3*0.1         # [mM]    #Fei *0.1!!! junction reduction factor
    Pd['koff_sll'] = 1300e-3               # [1/ms]
    Pd['kon_sll'] = 100                    # [1/mM/ms]
    Pd['Bmax_SLhighsl'] = 13.4e-3          # [mM] 
    Pd['Bmax_SLhighj'] = 1.65e-3*0.1       # [mM] #Fei *0.1!!! junction reduction factor
    Pd['koff_slh'] = 30e-3                 # [1/ms]
    Pd['kon_slh'] = 100                    # [1/mM/ms]
    Pd['Bmax_Csqn'] = 140e-3               # [mM] # Bmax_Csqn = 2.6      # Csqn buffering
    Pd['koff_csqn'] = 65                   # [1/ms] 
    Pd['kon_csqn'] = 100                   # [1/mM/ms] 
    Pd['GNaL'] = 0.0025*Pd['AF']
    Pd['tauhl'] = 600
    
    # Mark all states as dynamic ODEs:
    Pd['dynamic'] = [1]*42
 
    return Pd

# Define the atrial initial condition:
def Initialize_atrial(y0 = None):
     
    if y0 is None:
        mo=1.405627e-3
        ho= 9.867005e-1
        jo=9.915620e-1 
        do=7.175662e-6 
        fo=1.000681 
        fcaBjo=2.421991e-2
        fcaBslo=1.452605e-2 
        xtofo=4.051574e-3 
        ytofo= 9.945511e-1 
        xkro=8.641386e-3 
        xkso= 5.412034e-3
        RyRro=8.884332e-1
        RyRoo=8.156628e-7 
        RyRio=1.024274e-7 
        NaBjo=3.539892
        NaBslo=7.720854e-1 
        TnCLo=8.773191e-3 
        TnCHco=1.078283e-1 
        TnCHmo=1.524002e-2 
        CaMo=2.911916e-4 
        Myoco=1.298754e-3 
        Myomo=1.381982e-1
        SRBo=2.143165e-3 
        SLLjo=9.566355e-3 
        SLLslo=1.110363e-1 
        SLHjo=7.347888e-3 
        SLHslo=7.297378e-2 
        Csqnbo= 1.242988
        Ca_sro=0.01 
        Najo=9.136 
        Naslo=9.136 
        Naio=9.136
        Kio=120 
        Cajo=1.737475e-4 
        Caslo= 1.031812e-4 
        Caio=8.597401e-5 
        Vmo=-8.09763e+1 
        rkuro = 0	
        skuro = 1.0
        mlo = 1.0
        hlo = 0
        INalo = 0

        y0 = [mo, ho, jo, do, fo, fcaBjo, fcaBslo, xtofo, ytofo, xkro, xkso,RyRro, 
              RyRoo, RyRio, NaBjo, NaBslo, TnCLo, TnCHco, TnCHmo, CaMo, Myoco, Myomo,
              SRBo, SLLjo, SLLslo, SLHjo, SLHslo, Csqnbo,Ca_sro, Najo, Naslo, Naio, Kio, 
              Cajo, Caslo, Caio, Vmo, rkuro, skuro, mlo, hlo, INalo]
        
        return y0       
    
    else:
        return y0 

def name2index_atrial(name):
    """Take the name of a state in the model, return the index of that state in the solution vector y."""  
    state_names = ["mo", "ho", "jo", "do", "fo", "fcaBjo:", "fcaBslo", 
               "xtofo", "ytofo", "xkro", "xkso", "RyRro", "RyRoo", "RyRio",
               "NaBjo", "NaBslo:", "TnCLo", "TnCHco", "TnCHmo", "CaMo", "Myoco", "Myomo",
               "SRBo", "SLLjo", "SLLslo", "SLHjo", "SLHslo", "Csqnbo","Ca_sro","Najo","Naslo",
               "Naio","Kio","Cajo","Caslo","Caio","Vmo","rkuro","skuro",
               "mlo","hlo","INalo"]
    if type(name) == str:
        try:
            return state_names.index(name)
        except ValueError:
            raise ValueError("{} is not a state in the model".format(name))
    else:
        raise TypeError("Input must be the name of a state in the model as a str")
        
def index2name_atrial(index):
    state_names = ["mo", "ho", "jo", "do", "fo", "fcaBjo:", "fcaBslo", 
               "xtofo", "ytofo", "xkro", "xkso", "RyRro", "RyRoo", "RyRio",
               "NaBjo", "NaBslo:", "TnCLo", "TnCHco", "TnCHmo", "CaMo", "Myoco", "Myomo",
               "SRBo", "SLLjo", "SLLslo", "SLHjo", "SLHslo", "Csqnbo","Ca_sro","Najo","Naslo",
               "Naio","Kio","Cajo","Caslo","Caio","Vmo","rkuro","skuro",
               "mlo","hlo","INalo"]
    if type(index) == int:
        return state_names[index]
    else:
        raise TypeError("Input must be the index of a state as an int")   